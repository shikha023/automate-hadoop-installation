#!/usr/bin/python36


print("ContentType: text/html \n ")

import subprocess as sp




cmd="""
- hosts: server1
  tasks:
  - name: "install file"
    file: 
        state: directory
        path: /server1
        mode: 0777
#  - name: "get java software"
#    get_url:
#        url:
#        dest: /server1/
#
  - name: "scp software"
    copy:
        src: "{{ item }}"
        dest: /server1/
    with_items:
        - /var/www/cgi-bin/uploads/jdk-8u171-linux-x64.rpm
        - /var/www/cgi-bin/uploads/hadoop-1.2.1-1.x86_64.rpm 


  - name: "install java"
    command: "rpm -ivh /server1/jdk-8u171-linux-x64.rpm"
    ignore_errors: true
  - name: path set
    lineinfile:
        line: "{{ item }}"
        path: /root/.bashrc
    with_items:
        - export JAVA_HOME=/usr/java/jdk1.8.0_171-amd64/
        - export PATH=/usr/java/jdk1.8.0_171-amd64/bin:$PATH
#  - name: " get hadoop software"
#    get_url:
#        url:
#        dest: /server1/
  - name: install hadoop
    command: "rpm -ivh  /server1/hadoop-1.2.1-1.x86_64.rpm  --force"
    ignore_errors: true
  



- hosts: nn_server1
  tasks:

  - name: "make file"
    file: 
        state: directory
        path: /namenode
        mode: 0777
  - name: "hadoop core-configuration file"
    blockinfile:
        path: /etc/hadoop/core-site.xml
        block: |
          <property>
          <name>fs.default.name</name>
          <value>192.168.43.186:9001</value>
          </property>

        insertafter: <configuration>
        marker: ""


  - name: "hadoop hdfs file"
    blockinfile:
        path: /etc/hadoop/hdfs-site.xml
        block: |
          <property>
          <name>dfs.name.dir</name>
          <value>/namenode</value>
          </property>

        insertafter: <configuration>
        marker: ""


  - name: "format name-node"
    command: "echo Y | hadoop namenode -format"
  - name: "start hadoop service"
    command: "hadoop-daemon.sh start namenode"


- hosts: dn_server1
  tasks:

  - name: "make file"
    file: 
        state: directory
        path: /datanode
        mode: 0777
  - name: "hadoop core-file"
    blockinfile:
        path: /etc/hadoop/core-site.xml
        block: |
          <property>
          <name>fs.default.name</name>
          <value>192.168.43.186:9001</value>
          </property>

        insertafter: <configuration>
        marker: ""



  - name: "hadoop hdfs-file"
    blockinfile:
        path: /etc/hadoop/hdfs-site.xml
        block: |
          <property>
          <name>dfs.name.dir</name>
          <value>/datanode</value>
          </property>

        insertafter: <configuration>
        marker: ""



  - name: "datanode service"
    command: "hadoop-daemon.sh start datanode"

        
- hosts: jt_server1
  tasks:
  - name: "set mapred conf file"
    blockinfile:
        path: /etc/hadoop/mapred-site.xml
        block: |
          <property>
          <name>mapred.job.tracker</name>
          <value>192.168.43.186:9002</value>
          </property>

        insertafter: <configuration>
        marker: ""


  
  - name: "jt core-configuration file"
    blockinfile:
        path: /etc/hadoop/core-site.xml
        block: |
          <property>
          <name>fs.default.name</name>
          <value>192.168.43.186:9001</value>
          </property>

        insertafter: <configuration>
        marker: ""


  - name: "jobtracker service"
    command: "hadoop-daemon.sh start jobtracker"

- hosts: tt_server1
  tasks:
 
  - name: "set mapred conf file"
    blockinfile:
        path: /etc/hadoop/mapred-site.xml
        block: |
          <property>
          <name>mapred.job.tracker</name>
          <value>192.168.43.186:9002</value>
          </property>

        insertafter: <configuration>
        marker: ""


  
  - name: "tasktracker service"
    command: "hadoop-daemon.sh start tasktracker"

"""


f=open('./server1_w.yml','w')
f.write(cmd)
f.close()

o=sp.getstatusoutput("sudo ansible-playbook server1_w.yml")
print(o)
