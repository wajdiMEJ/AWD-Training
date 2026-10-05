const app = require('./app');
const { Eureka } = require('eureka-js-client');

const PORT = process.env.PORT || 8083;
const eurekaClient = new Eureka({
  instance: {
    app: 'MEETING',
    hostName: 'localhost',
    ipAddr: '127.0.0.1',
    port: {
      '$': Number(PORT),
      '@enabled': 'true',
    },
    vipAddress: 'meeting',
    statusPageUrl: `http://localhost:${PORT}/api/meetings/hello`,
    healthCheckUrl: `http://localhost:${PORT}/api/meetings/hello`,
    dataCenterInfo: {
      '@class': 'com.netflix.appinfo.InstanceInfo$DefaultDataCenterInfo',
      name: 'MyOwn',
    },
  },
  eureka: {
    host: 'localhost',
    port: 8761,
    servicePath: '/eureka/apps/',
  },
});

const server = app.listen(PORT, () => {
  console.log(`meeting microservice running on http://localhost:${PORT}`);
  console.log(`Swagger UI: http://localhost:${PORT}/swagger-ui`);
  eurekaClient.start();
});

function shutdown() {
  eurekaClient.stop();
  server.close(() => process.exit(0));
}

process.once('SIGINT', shutdown);
process.once('SIGTERM', shutdown);
