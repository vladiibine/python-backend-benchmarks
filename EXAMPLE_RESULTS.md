Overall results
----
| Running just one database query per request (/1q/)|Requests per second for concurrency 1|RPS for concurrency 10|RPS for concurrency 100|
|---|----|----|----|
|django|52.81|56.30|53.62|
|tornado|130.26|141.69|136.29 |
|flask|59.12|63.78|63.48|


Testing django
--------------
concurrency 100 -> 53.62 requests per second
```
$ ab -t10 -c100 http://0:9001/1q/             
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 537 requests


Server Software:        gunicorn/19.9.0
Server Hostname:        0
Server Port:            9001

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      100
Time taken for tests:   10.015 seconds
Complete requests:      537
Failed requests:        0
Total transferred:      102030 bytes
HTML transferred:       1074 bytes
Requests per second:    53.62 [#/sec] (mean)
Time per request:       1865.044 [ms] (mean)
Time per request:       18.650 [ms] (mean, across all concurrent requests)
Transfer rate:          9.95 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   3.9      0      13
Processing:   190 1701 403.6   1756    2167
Waiting:      189 1700 403.6   1755    2166
Total:        203 1703 400.3   1756    2167

Percentage of the requests served within a certain time (ms)
  50%   1756
  66%   1773
  75%   1805
  80%   1846
  90%   2129
  95%   2155
  98%   2163
  99%   2164
 100%   2167 (longest request)
```

concurrency 10 -> 56.30 RPS
```
$ ab -t10 -c10 http://0:9001/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 563 requests


Server Software:        gunicorn/19.9.0
Server Hostname:        0
Server Port:            9001

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      10
Time taken for tests:   10.001 seconds
Complete requests:      563
Failed requests:        0
Total transferred:      106970 bytes
HTML transferred:       1126 bytes
Requests per second:    56.30 [#/sec] (mean)
Time per request:       177.634 [ms] (mean)
Time per request:       17.763 [ms] (mean, across all concurrent requests)
Transfer rate:          10.45 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.3      0       2
Processing:    68  176   9.5    175     223
Waiting:       68  175   9.5    175     222
Total:         71  176   9.4    175     223

Percentage of the requests served within a certain time (ms)
  50%    175
  66%    177
  75%    178
  80%    179
  90%    183
  95%    191
  98%    195
  99%    199
 100%    223 (longest request)

```

concurrency 1 -> 52.81 RPS
```
$ ab -t10 -c1 http://0:9001/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 529 requests


Server Software:        gunicorn/19.9.0
Server Hostname:        0
Server Port:            9001

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      1
Time taken for tests:   10.017 seconds
Complete requests:      529
Failed requests:        0
Total transferred:      100510 bytes
HTML transferred:       1058 bytes
Requests per second:    52.81 [#/sec] (mean)
Time per request:       18.936 [ms] (mean)
Time per request:       18.936 [ms] (mean, across all concurrent requests)
Transfer rate:          9.80 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       4
Processing:    16   19   1.6     18      32
Waiting:       16   18   1.6     17      31
Total:         17   19   1.7     18      32

Percentage of the requests served within a certain time (ms)
  50%     18
  66%     19
  75%     19
  80%     20
  90%     20
  95%     22
  98%     23
  99%     27
 100%     32 (longest request)
```


Todnado
------
concurrency 100 -> 136.29 requests per second
```
$ ab -t10 -c100 http://0:9002/1q/                             (master)
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 1363 requests


Server Software:        TornadoServer/5.1.1
Server Hostname:        0
Server Port:            9002

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      100
Time taken for tests:   10.001 seconds
Complete requests:      1363
Failed requests:        0
Total transferred:      267148 bytes
HTML transferred:       2726 bytes
Requests per second:    136.29 [#/sec] (mean)
Time per request:       733.716 [ms] (mean)
Time per request:       7.337 [ms] (mean, across all concurrent requests)
Transfer rate:          26.09 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   2.6      0      16
Processing:   337  708  86.5    689    1034
Waiting:      336  707  86.5    688    1034
Total:        352  709  86.1    689    1049

Percentage of the requests served within a certain time (ms)
  50%    689
  66%    702
  75%    707
  80%    719
  90%    809
  95%    897
  98%    966
  99%    968
 100%   1049 (longest request)
```

concurrency 10 -> 141.69 requests per second
```
$ ab -t10 -c10 http://0:9002/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 1417 requests


Server Software:        TornadoServer/5.1.1
Server Hostname:        0
Server Port:            9002

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      10
Time taken for tests:   10.001 seconds
Complete requests:      1417
Failed requests:        0
Total transferred:      277732 bytes
HTML transferred:       2834 bytes
Requests per second:    141.69 [#/sec] (mean)
Time per request:       70.577 [ms] (mean)
Time per request:       7.058 [ms] (mean, across all concurrent requests)
Transfer rate:          27.12 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0       3
Processing:    28   70   7.2     68      97
Waiting:       28   70   7.2     68      97
Total:         30   70   7.2     68      98

Percentage of the requests served within a certain time (ms)
  50%     68
  66%     72
  75%     74
  80%     75
  90%     80
  95%     85
  98%     89
  99%     93
 100%     98 (longest request)

```

concurrency 1 -> 130.26 requests per second
```
$ ab -t10 -c1 http://0:9002/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 1303 requests


Server Software:        TornadoServer/5.1.1
Server Hostname:        0
Server Port:            9002

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      1
Time taken for tests:   10.003 seconds
Complete requests:      1303
Failed requests:        0
Total transferred:      255388 bytes
HTML transferred:       2606 bytes
Requests per second:    130.26 [#/sec] (mean)
Time per request:       7.677 [ms] (mean)
Time per request:       7.677 [ms] (mean, across all concurrent requests)
Transfer rate:          24.93 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       2
Processing:     5    7  18.2      6     656
Waiting:        2    7  18.2      6     655
Total:          6    8  18.2      7     656

Percentage of the requests served within a certain time (ms)
  50%      7
  66%      7
  75%      7
  80%      7
  90%      8
  95%      8
  98%     10
  99%     16
 100%    656 (longest request)
```

Flask
-----
concurrency 100 -> 63.48 requests per second
```
$ ab -t10 -c100 http://0:9003/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 635 requests


Server Software:        gunicorn/19.9.0
Server Hostname:        0
Server Port:            9003

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      100
Time taken for tests:   10.003 seconds
Complete requests:      635
Failed requests:        0
Total transferred:      102235 bytes
HTML transferred:       1270 bytes
Requests per second:    63.48 [#/sec] (mean)
Time per request:       1575.302 [ms] (mean)
Time per request:       15.753 [ms] (mean, across all concurrent requests)
Transfer rate:          9.98 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   3.4      0      15
Processing:    45 1451 329.2   1555    1645
Waiting:       45 1451 329.2   1554    1644
Total:         60 1453 325.9   1555    1645

Percentage of the requests served within a certain time (ms)
  50%   1555
  66%   1565
  75%   1575
  80%   1577
  90%   1623
  95%   1637
  98%   1642
  99%   1643
 100%   1645 (longest request)
```

concurrency 10 -> 63.78 requests per second
```
$ ab -t10 -c10 http://0:9003/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 638 requests


Server Software:        gunicorn/19.9.0
Server Hostname:        0
Server Port:            9003

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      10
Time taken for tests:   10.003 seconds
Complete requests:      638
Failed requests:        0
Total transferred:      102718 bytes
HTML transferred:       1276 bytes
Requests per second:    63.78 [#/sec] (mean)
Time per request:       156.787 [ms] (mean)
Time per request:       15.679 [ms] (mean, across all concurrent requests)
Transfer rate:          10.03 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       1
Processing:    20  155  11.1    155     178
Waiting:       20  155  11.1    155     177
Total:         21  156  11.0    155     178

Percentage of the requests served within a certain time (ms)
  50%    155
  66%    157
  75%    158
  80%    159
  90%    162
  95%    166
  98%    173
  99%    175
 100%    178 (longest request)
```

concurrency 1  -> 59.12 requests per second
```
ab -t10 -c1 http://0:9003/1q/
This is ApacheBench, Version 2.3 <$Revision: 1706008 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 0 (be patient)
Finished 592 requests


Server Software:        gunicorn/19.9.0
Server Hostname:        0
Server Port:            9003

Document Path:          /1q/
Document Length:        2 bytes

Concurrency Level:      1
Time taken for tests:   10.013 seconds
Complete requests:      592
Failed requests:        0
Total transferred:      95312 bytes
HTML transferred:       1184 bytes
Requests per second:    59.12 [#/sec] (mean)
Time per request:       16.913 [ms] (mean)
Time per request:       16.913 [ms] (mean, across all concurrent requests)
Transfer rate:          9.30 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.1      0       2
Processing:    15   17   1.1     16      25
Waiting:       14   16   1.1     16      24
Total:         15   17   1.1     16      25

Percentage of the requests served within a certain time (ms)
  50%     16
  66%     17
  75%     17
  80%     17
  90%     18
  95%     19
  98%     20
  99%     21
 100%     25 (longest request)
```