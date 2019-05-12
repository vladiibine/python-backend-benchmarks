This  repo helps test different webapp stacks under different conditions (loads)

Installation
------------
```
    $ cp .env.template .env

    # OPTIONAL: do any modifications to the .env parameters if you'd like
    
    $ docker-compose up
```

Running the benchmarks
---------------
This is an example of how to benchmarks, using the `ab` (apache benchmark) tool
``` 
    # This tests django
    $ ab -t10 -c10 http://localhost:9001/1q/
    
    # Use port 9002 for tornado, and 9003 for flask
```