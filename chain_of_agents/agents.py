from typing import List, Optional, Iterator, Dict
from mistralai import Mistral, UserMessage
import os
os.environ["MISTRAL_API_KEY"]= "***REMOVED***"
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-2402"

class WorkerAgent:
    """Worker agent that processes individual chunks of text."""
    
    def __init__(self, model: str, system_prompt: str):
        """
        Initialize a worker agent.
        
        Args:
            model: The LLM model to use (e.g., "gpt-3.5-turbo")
            system_prompt: The system prompt that defines the worker's role
        """
        self.model = model
        self.system_prompt = system_prompt
        #self.client = Together()  # Uses TOGETHER_API_KEY from environment
        self.client = Mistral(api_key=api_key)  # Uses MISTRAL_API_KEY from environment
        
    
    def process_chunk(self, chunk: str, query: str, previous_cu: Optional[str] = None) -> str:
        """
        Process a single chunk of text.
        
        Args:
            chunk: The text chunk to process
            query: The user's query
            previous_cu: The previous Cognitive Unit (CU) if any
            
        Returns:
            str: The processed output for this chunk
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Chunk: {chunk}\nQuery: {query}\nPrevious CU: {previous_cu or 'None'}"}
        ]
        
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=0
        )
        
        return response.choices[0].message.content
    
    async def process_chunk_stream(self, chunk: str, query: str, previous_cu: Optional[str] = None) -> Iterator[str]:
        """Process a chunk with streaming (for future implementation)."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Chunk: {chunk}\nQuery: {query}\nPrevious CU: {previous_cu or 'None'}"}
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class ManagerAgent:
    """Manager agent that synthesizes outputs from worker agents."""
    
    def __init__(self, model: str, system_prompt: str):
        """
        Initialize a manager agent.
        
        Args:
            model: The LLM model to use (e.g., "gpt-4")
            system_prompt: The system prompt that defines the manager's role
        """
        self.model = model
        self.system_prompt = system_prompt
        #self.client = Together()  # Uses TOGETHER_API_KEY from environment
        self.client = Mistral(api_key=api_key)  # Uses MISTRAL_API_KEY from environment

    
    def synthesize(self, worker_outputs: List[str], query: str) -> str:
        """
        Synthesize outputs from multiple worker agents.
        
        Args:
            worker_outputs: List of outputs from worker agents
            query: The original user query
            
        Returns:
            str: The final synthesized response
        """
        combined_outputs = "\n\n".join(f"Worker {i+1}: {output}" 
                                     for i, output in enumerate(worker_outputs))
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Worker Outputs:\n{combined_outputs}\n\nQuery: {query}"}
        ]
        
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=0
        )
        
        return response.choices[0].message.content
    
    async def synthesize_stream(self, worker_outputs: List[str], query: str) -> Iterator[str]:
        """Synthesize with streaming (for future implementation)."""
        combined_outputs = "\n\n".join(f"Worker {i+1}: {output}" 
                                     for i, output in enumerate(worker_outputs))
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Worker Outputs:\n{combined_outputs}\n\nQuery: {query}"}
        ]
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            stream=True
        )
        
        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content 