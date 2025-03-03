# thumbsup

AstrBot 插件 - 给你点赞

这是一个用于 AstrBot 的插件，允许用户通过简单的命令来点赞。

## 描述

该插件允许用户通过发送 `/赞我` 命令来触发点赞功能。插件会根据配置文件中的设置，自动为用户点赞并回复自定义消息。

## 安装

1. 克隆此仓库到你的 AstrBot 插件目录：
    ```sh
    git clone https://github.com/miaoxutao123/astrbot_plugin_thumbsUp
    ```

2. 确保在 AstrBot 的配置文件中启用了此插件。

## 配置

插件的配置包含以下配置项：

- `thnum`: 一次性点赞次数，默认值为 10。
- `response_str`： 自定义回复内容，默认值为 "已赞"。

## 使用

在聊天中发送 `/赞我` 命令即可触发插件的点赞功能。

