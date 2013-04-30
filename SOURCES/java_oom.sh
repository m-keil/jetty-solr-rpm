#!/bin/sh
#

echo `date` | mail -s "Java Error: OutOfMemory - $HOSTNAME" notify@domain.com
