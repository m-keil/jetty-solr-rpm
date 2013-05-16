#!/bin/sh
solrversion="4.3.0"
jettyversion="8.1.10.v20130312"
slf4jversion="1.7.5"
logbackversion="1.0.13"

rm -rf BUILD BUILDROOT tmp || true
mkdir -p BUILD BUILDROOT RPMS SRPMS

if [ ! -f SOURCES/solr-$solrversion.tgz ];
then
    wget "http://www.us.apache.org/dist/lucene/solr/$solrversion/solr-$solrversion.tgz" -O SOURCES/solr-$solrversion.tgz
    wget "http://www.us.apache.org/dist/lucene/solr/$solrversion/solr-$solrversion.tgz.md5" -O SOURCES/solr-$solrversion.tgz.md5
fi

if [ ! -f SOURCES/jetty-distribution-$jettyversion.tar.gz ];
then
    wget "http://download.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz" -O SOURCES/jetty-distribution-$jettyversion.tar.gz
    wget "http://download.eclipse.org/jetty/$jettyversion/dist/jetty-distribution-$jettyversion.tar.gz.md5" -O SOURCES/jetty-distribution-$jettyversion.tar.gz.md5
fi

if [ ! -f SOURCES/slf4j-$slf4jversion.tar.gz ];
then
    wget "http://www.slf4j.org/dist/slf4j-$slf4jversion.tar.gz" -O SOURCES/slf4j-$slf4jversion.tar.gz
fi

if [ ! -f SOURCES/logback-$logbackversion.tar.gz ];
then
    wget "http://logback.qos.ch/dist/logback-$logbackversion.tar.gz" -O SOURCES/logback-$logbackversion.tar.gz
fi


rpmbuild -ba --target=noarch --define="_topdir $PWD" --define="_tmppath $PWD/tmp" --define="sver $solrversion" --define="jver $jettyversion" --define="slfver $slf4jversion" --define="lver $logbackversion" jetty-solr.spec
