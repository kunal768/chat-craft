from langchain_community.document_loaders import PyPDFLoader, CSVLoader, Docx2txtLoader, UnstructuredHTMLLoader
from langchain_core.documents import Document
from app.core.utils.utils import get_file_type

class DocumentLoaders:
    def __init__(self):
        self.pdf_loader = None
        self.csv_loader = None
        self.docx_loader = None
        self.html_loader = None
        
    async def parse_doc(self, file_path: str) ->  list[Document]:
        file_type = get_file_type(file_path)
        content = None
        if file_type == '.pdf':
            if not self.pdf_loader:
                self.pdf_loader = PyPDFLoader(file_path=file_path)
            content =  await self.pdf_loader.aload()
            
            # reset 
            self.pdf_loader = None

        elif file_type == '.csv':
            if not self.csv_loader:
                self.csv_loader = CSVLoader(file_path=file_path)

            # Use self.csv_loader to parse CSV
            content =  await self.csv_loader.aload()

            # reset 
            self.csv_loader = None


        elif file_type == '.docx':
            if not self.docx_loader:
                self.docx_loader = Docx2txtLoader(file_path=file_path)
            # Use self.docx_loader to parse DOCX
            content =  await self.docx_loader.aload()

            # reset 
            self.docx_loader = None

        elif file_type == '.html':
            if not self.html_loader:
                self.html_loader = UnstructuredHTMLLoader(file_path=file_path)
            # Use self.html_loader to parse HTML
            content =  await self.html_loader.aload()

            # reset 
            self.html_loader = None
            
        else:
            raise ValueError(f'Unsupported file type: {file_type}')
    
        if not content:
            raise ValueError(f"Error loading file : {file_path}")
        
        return content



