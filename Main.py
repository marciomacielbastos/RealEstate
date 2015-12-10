# -*- coding: utf-8 -*-

__author__ = 'marcio'

# res = Growth('/tmp/AcrisInPluto.csv', '/home/marcio/Marcio/timeseries.csv', '/tmp/bbs.csv', 3, 6)
# res.growth(6)
a = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
kernel = 4
offset = len(a) % kernel
if offset:
    t = (len(a) / kernel)
else:
    t = len(a) / kernel
end = 0
for i in xrange(kernel):
    begin = end
    end = end+t
    if offset:
        end += 1
        offset -= 1
    k = a[begin:end]
    if end > len(a):
        end = len(a)
    print k


