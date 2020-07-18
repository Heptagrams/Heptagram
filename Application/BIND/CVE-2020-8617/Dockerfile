FROM centos:7
MAINTAINER knqyf263

ENV version 9.12.4

# Install packages
RUN yum -y update \
    && yum -y groupinstall "Development Tools" \
    && yum install -y epel-release \
    && yum -y install kernel-devel kernel-headers openssl-devel perl-Net-DNS wget bind-utils vim tar python-pip \
    && pip install --upgrade pip && pip install argparse ply

# Install BIND9 from source
RUN cd /usr/local/src && \
    wget ftp://ftp.isc.org/isc/bind9/${version}/bind-${version}.tar.gz && \
    tar zxvf bind-${version}.tar.gz && \
    mv bind-${version} bind && \
    rm bind-${version}.tar.gz
RUN cd /usr/local/src/bind && \
    ./configure --enable-syscalls --prefix=/var/named/chroot --enable-threads --with-openssl=yes --enable-openssl-version-check --enable-ipv6 --disable-linux-caps && \
    chown -R root:root /usr/local/src/bind && \
    make && \
    make install

# Create device files
RUN mkdir /var/named/chroot/dev && \
    mknod -m 666 /var/named/chroot/dev/null c 1 3 && \
    mknod -m 666 /var/named/chroot/dev/random c 1 8

# Create rndc key
RUN /var/named/chroot/sbin/rndc-confgen -a

RUN mkdir /var/named/chroot/data && \
    mkdir /var/named/chroot/var/log && \
    mkdir /var/named/chroot/var/named

# Create hint file
RUN cd /var/named/chroot/var/named && \
    wget ftp://ftp.nic.ad.jp/internet/rs.internic.net/domain/named.root

# Add files
ADD ./contents/named.conf /var/named/chroot/etc/named.conf
ADD ./contents/named /etc/sysconfig/named
ADD ./contents/example.com.zone /var/named/chroot/var/named/example.com.zone

# Create symbolic link
RUN ln -s /var/named/chroot/etc/rndc.key /etc/rndc.key && \
    ln -s /var/named/chroot/etc/named.conf /etc/named.conf

EXPOSE 53 953

CMD ["/var/named/chroot/sbin/named", "-g", "-t", "/var/named/chroot", "-c", "/etc/named.conf"]

