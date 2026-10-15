from motor.motor_asyncio import AsyncIOMotorClient


async def ping_server(uri : str) -> AsyncIOMotorClient | Exception:

  # Create a new client and connect to the server
  client = AsyncIOMotorClient(uri)

  # Send a ping to confirm a successful connection
  try:
      await client.admin.command('ping')
      print("Pinged your deployment. You successfully connected to MongoDB!")
      return client 
  except Exception as e:
      print(e)
      raise e
      
