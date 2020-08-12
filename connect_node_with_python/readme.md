## Guide on how to connect node and python

we can use AsyncProcessServer to connect node with python.
AsyncProcessServer will run new process on node that can run any program from python to any other language.
After that we need to setup standard way to write output on python such that it will redirect to the node main process manager.
We can do that with FileDescriptor object in python.
FileDescriptor is lowest level of I/O operation in python that run I/O operations directly with machine kernals.

```node
const chat_engine = new AsyncProcessServer({
  argv: ["python3", "multichat.py", "arg", "arg_value", "arg", "arg_value"],
  fd_arg: "--fd",
  wait_for: "READY",
});
```

with only this simple one line of code we can connect node with python.
Next part we have to redirect communication from python to node.

We can use python file Descriptor to redirect communication from python to node. fd_arg in above node.js code is file Descriptor argument.
So that your python program must accept that `--fd` arg to use that file descriptor value provided by node.

After that you have to point input and output stream to that file descriptor value. Below you will see on how to do that.

```python

print('got fd {}'.format(opt['fd']), flush=True)
os.set_blocking(opt['fd'], True)
out_stream = os.fdopen(opt['fd'], 'wb', buffering=0)
in_stream = os.fdopen(opt['fd'], 'r')

```

and now whenever you want to send message to or receive message from node you wanna use that in and out stream object.
below i will show you how to send message back and forth from node to python and python to node.

send message or receive message in python

```python

def write_response_json(response_json): # send message to node
  out_stream.write(bytearray(json.dumps(response_json, 'utf-8')))

line = in_stream.readline() # receive message from node and store in line
```

send message or receive message in node.js

```node.js
hat_engine.request(this.req_json, (err, res_json) => {
  if (err) {
    res.writeHead(500, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ message: err.toString() }));
    return;
  }
  res_json.session_id = req_json.session_id;
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ message: err.toString() }));
});
```
