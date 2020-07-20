# device_guardian_server

A REST api server written in Python3 using FastAPI framework.

Poses as an application server for device_guardian project.

It handles user registration and auth and takes care of pairing mobile app with protected devices which then report security events through this server to the app.
The mobile app can propagate events like locking the screen or power off to paired devices.