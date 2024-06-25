from services.tool_registry import ToolFile
from services.logger import setup_logger
from features.quizzify.tools import RAGpipeline
from features.quizzify.tools import QuizBuilder
from api.error_utilities import LoaderError, ToolExecutorError
import uuid

logger = setup_logger()

def executor(files: list[ToolFile], topic: str, num_questions: int, verbose=False):
    
    try:
        if verbose: logger.debug(f"Files: {files}")

        # Instantiate RAG pipeline with default values
        pipeline = RAGpipeline(verbose=verbose)
        print("--------------------------------RAG PIPELINE WORKS --------------------------------")
        pipeline.compile()
        print("--------------------------------PIPELINE COMPILER WORKS --------------------------------")
        print("---FILES---",files)
        # Process the uploaded files
        db = pipeline(files)
        print("--------------------------------PIPELINE WORKS --------------------------------")
        quiz_builder =QuizBuilder(db, topic, verbose=verbose).create_questions(num_questions)
        # Create and return the quiz questions
        output = quiz_builder
    
    except LoaderError as e:
        error_message = e
        logger.error(f"Error in RAGPipeline -> {error_message}")
        raise ToolExecutorError(error_message)
    
    except Exception as e:
        error_message = f"Error in executor: {e}"
        logger.error(error_message)
        raise ValueError(error_message)
    
    return output

