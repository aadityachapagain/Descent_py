const http = require("http");
const { AsyncProcessServer } = require("./async-process-server.js");

const INACTIVITY_TIMEOUT = 4 * 60 * 1000;
const LISTEN_PORT = 3000;

const chat_engine = new AsyncProcessServer({
  argv: ["python3", "multichat.py"],
  fd_arg: "--fd",
  wait_for: "READY",
});

function debug(msg) {
  console.log(msg);
}

const passwords_bcrypted = {
  embodied: "$2b$04$mAg0s4VxdlpJwBRu.8Q3nOzUtWDhwjmck7CQf5s2XZ90Rf4JGOCae",
};

function check_password(username, password, req, res, success_cb) {
  if (!passwords_bcrypted[username]) {
    res.writeHead(401, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: "bad username" }));
    return;
  }
  console.log("running bcrypt.ecompare");
  bcrypt.compare(password, passwords_bcrypted[username], function (
    err,
    result
  ) {
    if (!result) {
      res.writeHead(401, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: "bad username" }));
      return;
    }
    console.log("running success_cb");
    success_cb();
  });
}

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  console.log(`got request: ${url.pathname}`);
  if (url.pathname === "/check") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ code: "SUCCESS" }));
  } else if (url.pathname === "/interact") {
    const auth = basic_auth(req);
    if (!auth) {
      res.writeHead(401, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ message: "basic-auth required" }));
      return;
    }
    check_password(auth.name, auth.pass, req, res, () => {
      // allocate session id
      const incoming_data = [];
      req
        .on("data", (data) => {
          incoming_data.push(data);
        })
        .on("end", () => {
          try {
            const json_str = Buffer.concat(incoming_data).toString("utf-8");
            const req_json = JSON.parse(json_str);
            if (!req_json.session_id) {
              req_json.session_id = uuidv4();
            }

            //TODO: validate request

            chat_engine.request(this.req_json, (err, res_json) => {
              if (err) {
                res.writeHead(500, { "Content-Type": "application/json" });
                res.end(JSON.stringify({ message: err.toString() }));
                return;
              }
              res_json.session_id = req_json.session_id;
              res.writeHead(200, { "Content-Type": "application/json" });
              res.end(JSON.stringify({ message: err.toString() }));
            });
          } catch (err) {
            res.writeHead(500, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ message: err.toString() }));
          }
        });
    });
  } else {
    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: `not found: ${req.path}` }));
  }
});
console.log(`listening on port ${LISTEN_PORT}.`);
server.listen(LISTEN_PORT);
