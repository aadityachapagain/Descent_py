def recurse(level):
    print ('recurse(%s)' % level)
    if level:
        recurse(level-1)
    return

def not_called():
    print ('This function is never called.')


def main():
    print ('This is the main program.')
    recurse(2)
    return

if __name__ == '__main__':
    main()


# Its easy to trace with command line like this:
# python  -m trace --trace with_cmd.py

# Now trace with programming interface

import trace

tracer = trace.Trace(count=True, trace=True)
tracer.runfunc(recurse, 3)

results = tracer.results()
results.write_results(coverdir='coverdir2')