import aio_pika
from app.config import settings


class RabbitMQClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RabbitMQClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, host: str = settings.RABBITMQ_HOST, port: int = settings.RABBITMQ_PORT,
                 username: str = settings.RABBITMQ_USER, password: str = settings.RABBITMQ_PASSWORD):
        if not hasattr(self, 'initialized'):
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            self.connection = None
            self.initialized = True

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(
                f"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"
            )

    async def get_connection(self):
        if not self.connection or self.connection.is_closed:
            await self.connect()
        return self.connection

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
            self.connection = None

    async def publish(self, queue_name: str, message: str):
        connection = await self.get_connection()
        async with connection.channel() as channel:
            queue = await channel.declare_queue(queue_name)
            await channel.default_exchange.publish(
                aio_pika.Message(body=message.encode()),
                routing_key=queue_name,
            )

    async def consume(self, queue_name: str, callback):
        connection = await self.get_connection()
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)

        async def wrapped_callback(message: aio_pika.IncomingMessage):
            async with message.process():
                await callback(message)

        await queue.consume(wrapped_callback)
