from typing import Optional, List, Dict, Any
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from ..config import Config
from ..utils.logger import logger
import asyncio

class BaseAgent:
    def __init__(
        self,
        name: str,
        role: str,
        instructions: List[str],
        model_id: Optional[str] = None,
        temperature: Optional[float] = None,
        tools: Optional[List[Any]] = None
    ):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.model_id = model_id or Config.DEFAULT_MODEL_ID
        self.temperature = temperature or Config.DEFAULT_TEMPERATURE
        self.tools = tools or [YFinanceTools()]
        
        self.model = self._setup_model()
        self.agent = self._setup_agent()
        logger.info(f"Initialized {self.name} agent")
        
    def _setup_model(self) -> OpenAIChat:
        """Initialize the OpenAI chat model"""
        try:
            logger.info(f"Setting up OpenAI model {self.model_id}")
            model = OpenAIChat(
                id=self.model_id,
                api_key=Config.OPENAI_API_KEY,
                temperature=self.temperature
            )
            logger.info("Model setup complete")
            return model
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI model: {str(e)}")
            raise
            
    def _setup_agent(self) -> Agent:
        """Initialize the Agno agent"""
        try:
            logger.info("Setting up Agno agent")
            agent = Agent(
                name=self.name,
                role=self.role,
                model=self.model,
                instructions=self.instructions,
                description=f"{self.name} - {self.role}",
                add_datetime_to_instructions=True
            )
            logger.info("Agno agent setup complete")
            return agent
        except Exception as e:
            logger.error(f"Failed to initialize Agno agent: {str(e)}")
            raise
            
    async def execute(self, prompt: str, **kwargs) -> str:
        """Execute a prompt and return the response"""
        try:
            logger.info(f"Executing prompt: {prompt[:100]}...")
            response_gen = self.agent.run(prompt, stream=True, **kwargs)
            response = ""
            for chunk in response_gen:
                response += chunk.content
            logger.info("Successfully executed prompt")
            return response
        except Exception as e:
            logger.error(f"Error executing prompt: {str(e)}")
            raise
            
    async def execute_with_retry(
        self,
        prompt: str,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """Execute a prompt with retry mechanism"""
        retries = 0
        last_error = None
        
        while retries < max_retries:
            try:
                return await self.execute(prompt, **kwargs)
            except Exception as e:
                last_error = e
                retries += 1
                logger.warning(f"Retry {retries}/{max_retries} after error: {str(e)}")
                await asyncio.sleep(1)  # Add delay between retries
                
        logger.error(f"Failed after {max_retries} retries. Last error: {str(last_error)}")
        raise last_error
        
    def format_prompt(self, template: str, **kwargs) -> str:
        """Format a prompt template with variables"""
        try:
            # Replace ${variable} with {variable} for str.format()
            formatted_template = template
            for key in kwargs:
                formatted_template = formatted_template.replace(f"${{{key}}}", "{" + key + "}")
            return formatted_template.format(**kwargs)
        except KeyError as e:
            logger.error(f"Missing required variable in prompt template: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error formatting prompt: {str(e)}")
            raise 