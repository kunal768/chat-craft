from langchain_ollama import OllamaEmbeddings
from motor.motor_asyncio import AsyncIOMotorCollection

class FileSearchService:
    def __init__(self, embed_model : OllamaEmbeddings, collection : AsyncIOMotorCollection):
        self.embed_model = embed_model
        self.collection = collection
    
    async def vector_search(self, user_id: str, query: str, num_candidates : int =100, limit : int=5):
        try : 
            query_vector = await self.embed_model.aembed_query(query) 
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vectorsearch",
                        "path": "embedding",
                        "queryVector": query_vector,
                        "numCandidates": num_candidates,
                        "limit": limit,
                        "filter": {"user_id": user_id}
                    }
                }
            ]

            # Run aggregation asynchronously and get an async cursor
            cursor = self.collection.aggregate(pipeline)
            
            # Collect results asynchronously
            results = []
            async for doc in cursor:
                results.append(doc)
            
            # saves the cost by not using LLM and exiting early
            if not results :
                raise FileNotFoundError("could not find any result for query")
            
            return results
                    
        except Exception as e :
            raise e      
