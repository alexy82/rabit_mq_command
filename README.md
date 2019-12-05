# Message queue manager
## Command line
### Declare exchange with command line
 

**Syntax**
```commandline
python -m command.exchange <action> -f <file> -e <exchange_name>
```
virtualenv
```commandline
.venv/bin/python -m command.exchange <action> -f <file> -e <exchange_name>
```

|       |Kiểu dữ liệu  | Giải thích |Mặc định |
|--------|-----| -----|-----|
|action  |  String| chỉ được chọn:<br> **remove**: xóa exchange <br> **declare**: tạo exchange<br> **bind**: bind exchange      |  Bắt buộc |
|<pre>-f, --file</pre>     |String| đường dẫn 1 file config exchange <br> **Lưu ý:** <br> Phải là file json <br>Phải có field **declare** và **bind**  | Bắt buộc|
| <pre>-e, --exchange</pre>| String| tên exchange cụ thể thể thực hiện 1 action     |    tất cả exchange |


**Example**


Tạo exchange từ file **/vagrant/code/is_mq_manager/example_exchange_config.json**
```commandline
.venv/bin/python -m command.exchange declare -f /vagrant/code/is_mq_manager/example_exchange_config.json
```
```commandline
.venv/bin/python -m command.exchange declare --file /vagrant/code/is_mq_manager/example_exchange_config.json
```
## Declare queue with command line
 

**Syntax**
```commandline
python -m command.queue  <action> -f <file> -q <queue_name> -p <pattern> -e <if_empty> -u <if_unused>
```
virtualenv
```commandline
.venv/bin/python -m command.queue  <action> -f <file> -q <queue_name> -p <pattern> -e <if_empty> -u <if_unused>
```

|        | Kiểu dữ liệu | Giải thích |Mặc định |
|--------|-----| -----|-----|
|action   | String| chỉ được chọn:<br> **remove**: xóa queue  <br>**declare**: tạo queue<br> **bind**: bind queue <br> **purge**: purge queue     |  Bắt buộc |
|<pre>-f, --file</pre>    |String |đường dẫn 1 file config exchange <br> **Lưu ý:** <br> Phải là file json <br>Phải có field **declare** và **bind** | Bắt buộc|
| <pre>-q, --queue</pre>|String | tên queue cụ thể thể thực hiện 1 action     |    tất cả queue |
|<pre>-p, --pattern</pre>|String|Pattern để thực hiện 1 action với các queue hợp lệ với pattern<br> **Lưu ý** -q và -p không thể dùng chung|tất cả queue|
|<pre>-e, --empty</pre>|Boolean| if_empty chỉ dùng chung với action **remove** xóa các queue nếu queue đó không chưa message (rỗng)|False|
|<pre>-u, --unused</pre>|Boolean| if_unused chỉ dùng chung với action **remove** xóa các queue nếu không có consumer nào connect đến |False|


**Example**

Tạo queue **test** từ **/vagrant/code/is_mq_manager/example_queue_config.json**
```commandline
.venv/bin/python -m command.queue declare -f /vagrant/code/is_mq_manager/example_queue_config.json -q test
```
Tạo tất cả các queue từ **/vagrant/code/is_mq_manager/example_queue_config.json**
```commandline
.venv/bin/python -m command.queue declare -f /vagrant/code/is_mq_manager/example_queue_config.json 
```
xóa queue **test** nếu không có consumer connect đến
```commandline
.venv/bin/python -m command.queue remove -f /vagrant/code/is_mq_manager/example_queue_config.json  --queue test -u
```
<br>

### Send message with command line
**Syntax**
```commandline
python -m command.publisher -f <folder> -p <pattern> -r <routing_key_file>
```
virtualenv
```commandline
.venv/bin/python -m command.publisher -f <folder> -p <pattern> -r <routing_key_file>
```

|       |Kiểu dữ liệu  | Giải thích |Mặc định |
|--------|-----| -----|-----|
|<pre>-f, --folder</pre>     |String| Folder chứa các file message  | Bắt buộc|
|<pre>-p, --pattern</pre>  |  String| Bắn các message có routing_key hợp lệ với pattern   |  bắn tất cả mesage |
| <pre>-r, --routing-key-file</pre>| String| tên file messsage    |    bắn tất cả message|

**Example**

Bắn tất cả message trong folder **/vagrant/code/is_mq_manager/simulator/publisher/message_example/**
```commandline
.venv/bin/python -m command.publisher -f /vagrant/code/is_mq_manager/simulator/publisher/message_example/
```

Bắn message trong file **routing.key.example.json** từ folder **/vagrant/code/is_mq_manager/simulator/publisher/message_example/**
```commandline
.venv/bin/python -m command.publisher -f /vagrant/code/is_mq_manager/simulator/publisher/message_example/ -r routing.key.example.json
```
Bắn message trong folder **/vagrant/code/is_mq_manager/simulator/publisher/message_example/** với tên thỏa mãn pattern **routing***
```commandline
.venv/bin/python -m command.publisher  --folder /vagrant/code/is_mq_manager/simulator/publisher/message_example/ --pattern routing*
```

## Syntax file 
**Lưu ý**
Connection
- Nếu **type** là url thì chỉ cần field **url** ngược lại nếu là settings thì chỉ cần field **settings**
- Về Url value là một url connection
- Về settings value là tên của connection được define ở settings.py

ex:
```json

    {
          "connection_type": "url",
          "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
    }
```
```json
    {
          "connection_type": "setting",
          "setting": "default"
    }
```


**Yêu cầu**
 - File config bắt buộc phải là file JSON (.json)
 - Phải có field "declare" và "bind"


 **Syntax file json**
	


   ```json
{
"declare": {
    "name_exchange": {
      "type": "type_exchange",
      "config": {
        "passive": false,
        "durable": false,
        "auto_delete": false,
        "internal": false,
        "arguments": {}
      },
      "connection_type": "url or settings",
      "url": "connection url",
      "settings":"name connection in settings.py"
    }
    },
"bind":{
"name_exchange": [
      {
        "name": "name_exchange_bind_to",
        "routing_key": "routing key",
        "arguments": {}
      }]
      
}
 }
    
   ```
**Example**
example_exchange_config.json
```json
   {
  "declare": {
    "default": {
      "type": "topic",
      "config": {
        "passive": false,
        "durable": false,
        "auto_delete": false,
        "internal": false,
        "arguments": null
      },
      "connection_type": "url",
      "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
    },
    "long.test_exchange": {
      "type": "topic",
      "config": {
        "passive": false,
        "durable": true,
        "auto_delete": false,
        "internal": false,
        "arguments": null
      },
      "connection_type": "setting",
      "setting": "default"
    },
    "test": {
      "type": "fanout",
      "config": {
        "passive": false,
        "durable": false,
        "auto_delete": false,
        "internal": false,
        "arguments": null
      },
      "connection_type": "url",
      "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
    },
    "test1": {
      "type": "fanout",
      "config": {
        "passive": false,
        "durable": false,
        "auto_delete": false,
        "internal": false,
        "arguments": null
      },
      "connection_type": "url",
      "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
    }
  },
  "bind": {
    "default": [
      {
        "name": "test",
        "routing_key": "*.*.*",
        "arguments": null
      },
      {
        "name": "test2",
        "routing_key": "*.*.*",
        "arguments": null
      }
    ]
  }
}
```

<br>

 
 **Syntax Declare Queue**
 ```json
   {
    "declare": {
        "name_queue": {
            "config": {
                "passive": false,
                "durable": false,
                "exclusive": false,
                "auto_delete": false,
                "arguments": { }
            },
            "connection_type": "url or settings",
            "url": "connection url",
            "settings":"name connection in settings.py"
        }
     },
     "bind":{
     "test": [
            {
                "routing_key": "routing_key",
                "exchange": "exchange bind to",
                "arguments": {}
            }]
    }
   }
        
  ```
**Example**

example_queue_config.json	
```json
   {
    "declare": {
        "test": {
            "config": {
                "passive": false,
                "durable": false,
                "exclusive": false,
                "auto_delete": false,
                "arguments": {
                    "x-message-ttl": 10
                }
            },
            "connection_type": "url",
            "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
        },
        "test1": {
            "config": {
                "passive": false,
                "durable": true,
                "exclusive": false,
                "auto_delete": false,
                "arguments": null
            },
            "connection_type": "url",
            "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
        },
        "test2": {
            "config": {
                "passive": false,
                "durable": true,
                "exclusive": false,
                "auto_delete": false,
                "arguments": null
            },
            "connection_type": "url",
            "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
        }
    },
    "bind": {
        "test": [
            {
                "routing_key": "*.*.*",
                "exchange": "default",
                "arguments": null
            },
            {
                "routing_key": "*.*.*",
                "exchange": "test",
                "arguments": null
            }
        ],
        "test1": [
            {
                "routing_key": "*.*.*",
                "exchange": "default",
                "arguments": null
            },
            {
                "routing_key": "*.*.*",
                "exchange": "test",
                "arguments": null
            }
        ],
        "test2": [
            {
                "routing_key": "*.*.*",
                "exchange": "default",
                "arguments": null
            },
            {
                "routing_key": "*.*.*",
                "exchange": "test2",
                "arguments": null
            }
        ]
    }
}
 ```
### Create message files
>**Lưu ý**
> - Với phần exchanges mỗi key là tên exchange và config connection như config exchange
> - ex:
 ```json
    {
      "exchanges": {
        "default": {
          "connection_type": "url",
          "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
         }
      }
    }
 ```
    
>**Quy ước file**
> - Tên file là routing_key
> - Đặt các file vào trong một thư mục
> - File thõa mãn syntax dưới
> - Phải là file json hoặc xml
 
**Syntax json file**
```json
[
    {
        "exchanges": {},
        "messsage":
        [
          {
            "properties": {},
            "body": {}
          }
        ]
    }
]
```
**Example**
```json
{
  "exchanges": {
    "default": {
      "connection_type": "url",
      "url": "amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf"
    }
  },
  "messages": [
    {
      "properties": {
        "content-type": "application/json",
        "headers": {}
      },
      "body": {
        "field_a": "value_a",
        "field_b": "value_b"
      }
    },
    {
      "properties": {
        "content-type": "application/json",
        "headers": {}
      },
      "body": {
        "field_a": "value_c",
        "field_b": "value_d"
      }
    }
  ]
}

```
**Syntax xml file**
```xml
<root>
    <exchanges>  </exchanges>
    <messages>
        <properties>  </properties>
        <body> </body>
    </messages>
</root>
```
**Example**
```xml
<?xml version="1.0" ?>
<root>
    <exchanges>
        <default>
            <connection_type>url</connection_type>
            <url>amqp://rzblafqf:ZnUhFd1ElXuzsUpUNsmgV-GmCpiQxqkz@woodpecker.rmq.cloudamqp.com/rzblafqf</url>
        </default>
    </exchanges>
    <messages>
        <properties>
            <content-type>application/json</content-type>
            <headers></headers>

        </properties>
        <body>
            <field_1>test</field_1>

            <field_2>test</field_2>
        </body>
    </messages>
    <messages>
        <properties>
            <content-type>application/json</content-type>
            <headers></headers>

        </properties>
        <body>
            <field_1>test</field_1>

            <field_2>test</field_2>
        </body>
    </messages>
</root>
```
