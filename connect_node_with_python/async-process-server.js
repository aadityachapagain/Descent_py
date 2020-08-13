const child_process = require("child_process");
const socketpair = require("unix-socketpair");
const net = require("net");
const fs = require("fs");
const { fcntl, fcntl_constants } = require("fs-ext");

class AsyncProcessServer {
  constructor({ argv, wait_for, fd_arg }) {
    const child_options = {};
    let fds = undefined;
    const args = argv.slice(1);
    let exec_callback;
    if (fd_arg !== undefined) {
      fds = socketpair(socketpair.SOCK_STREAM);
      args.push(fd_arg);
      args.push(fds[1].toString());
      fcntl(fds[1], "setfd", 0); // remove close-on-exec
    } else {
      child_options.encoding = "buffer";
    }
    this.subproc = child_process.execFile(argv[0], args, child_options);
    if (!fds) {
      this.subproc.stdout.on("data", (data) => this.handle_incoming_data(data));
      this.subproc.stderr.on("data", (data) =>
        console.error(data.toString("utf-8").replace(/\n$/, ""))
      );
    } else {
      const socket = net.Socket({
        fd: fds[0],
        readable: true,
        writable: true,
        encoding: "binary",
      });
      socket.on("data", (data) => {
        // XXX: this should never happen!!!   so why is net.Socket creating a non-binary stream!?!?!?
        if (typeof data === "string") data = Buffer.from(data);

        this.handle_incoming_data(data);
      });
      fs.closeSync(fds[1]);
      this.subproc.stdout.on("data", console.log);
      this.subproc.stderr.on("data", console.error);
    }
    this.subproc.on("close", (code) => {
      console.log(`child process exited with code ${code}`);
    });
    this.buffered = [];
    this.wait_for = wait_for;
    this.next_req_id = 1;
    this.req_id_to_callback = {};
  }
  request(json, callback) {
    json.req_id = "R" + this.next_req_id++;
    this.subproc.stdin.write(JSON.stringify(json) + "\n");
    this.req_id_to_callback[json.req_id] = callback;
  }
  handle_incoming_data(data) {
    const first_nl = data.indexOf("\n");
    if (first_nl < 0) {
      this.buffered.push(data);
      return;
    }
    if (first_nl > 0) this.buffered.push(data.subarray(0, first_nl));
    try {
      const line = Buffer.concat(this.buffered).toString("utf-8");
      this.dispatch_line(line);
    } catch (err) {
      console.log("error parsing json");
    }
    let prev_nl = first_nl;
    for (;;) {
      let nl = data.indexOf("\n", prev_nl + 1);
      if (nl < 0) break;
      try {
        const subbuf = data.subarray(prev_nl + 1, nl);
        prev_nl = nl;
        const line = subbuf.toString("utf-8");
        this.dispatch_line(line);
      } catch (err) {}
    }

    if (prev_nl === data.length - 1) {
      this.buffered = [];
    } else {
      this.buffered = [data.subarray(prev_nl)];
    }
  }
  dispatch_line(line) {
    console.log(`dispatch_line: ${line}`);
    if (this.wait_for !== undefined) {
      if (this.wait_for === line) {
        this.wait_for = undefined;
      }
    } else if (line[0] != "{") {
      console.log(`from subprocess: ${line}`);
    } else {
      const json = JSON.parse(line);
      this.dispatch_json(json);
    }
  }
  dispatch_json(json) {
    const callback = this.req_id_to_callback[json.req_id];
    if (!callback) {
      console.log(`no request found for ${json.req_id}`);
      return;
    }
    delete this.req_id_to_callback[json.req_id];
    callback(null, json);
  }
}

exports.AsyncProcessServer = AsyncProcessServer;
