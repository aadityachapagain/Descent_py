#!/usr/bin/env python3

"""
Script for use by the remote-chat api server.

By default, this reads JSON line-by-line from standard-input,
processes it, then prints the result to standard-output.

The --fd option is how it is used in production:  it uses that
file-descriptor to replace stdin/stdout to communicate
with the parent process which manages the rest api.
"""

from parlai.core.params import ParlaiParser
from parlai.core.script import ParlaiScript, register_script
from parlai.core.agents import create_agent, create_agent_from_shared
from parlai.core.worlds import create_task
import parlai.utils.logging as logging
import random
import sys
import json
import os


def setup_args(parser=None):
    if parser is None:
        parser = ParlaiParser(True, True, 'multichat helper program')
    parser.add_argument(
        '--fd',
        type=int,
        help='file-descriptor for communication (default: use stdin/stdout)'
    )
    parser.set_defaults(interactive_mode=True, task='interactive')
    return parser


def multichat(opt):
    in_stream = sys.stdin
    out_stream = sys.stdout

    if opt['fd']:
        print('got fd {}'.format(opt['fd']), flush=True)
        os.set_blocking(opt['fd'], True)
        out_stream = os.fdopen(opt['fd'], 'wb', buffering=0)
        in_stream = os.fdopen(opt['fd'], 'r')

    #
    # Load the model and create a shared-agent object.
    #
    original_agent = create_agent(opt)
    shared_agent = original_agent.share()

    #
    # Indicate that we are ready to serve requests.
    #
    out_stream.write(b"READY\n")


    def write_response_json(response_json):
        out_stream.write(bytearray(json.dumps(response_json, 'utf-8')))

    #
    # Read JSON as lines of input.
    #
    # We only create agents that are chatbots; there is one per session.
    #
    agents_by_session_id = {}
    while True:
        line = in_stream.readline()
        if line is None:
            break
        try:
            request_json = json.loads(line)
        except:
            print("bad json line: {}".format(line))
            continue
        session_id = request_json["session_id"]
        req = request_json["req_id"]
        kill = request_json.get("kill", False)
        if kill:
            ex_agent = agents_by_session_id[session_id]
            ex_agent.shutdown()
            del agents_by_session_id[session_id]
            write_response_json({"req_id": req, "session_id": session_id, "killed": true})
            continue
        agent = agents_by_session_id.get(session_id)
        if agent is None:
            agent = create_agent_from_shared(shared_agent)
            agents_by_session_id[session_id] = agent

        #
        # OK, this is where we compute the response to an input chat message.
        #
        # Currently, we do this work on the main thread,
        # but a very small thread-pool could be a better approach.
        # The "req_id" allows the parent-process to handle responses out-of-order.
        #
        agent.observe({"text": request_json['text'], "episode_done": False})
        response = agent.act()
        response_text = response['text']
        response_json = {"req_id": req, "session_id": session_id, "text": response_text}
        self.write_response_json(response_json)


@register_script('multichat')
class Cmdline(ParlaiScript):
    @classmethod
    def setup_args(cls):
        return setup_args()

    def run(self):
        return multichat(self.opt)

if __name__ == '__main__':
    random.seed(42)
    Cmdline.main()

