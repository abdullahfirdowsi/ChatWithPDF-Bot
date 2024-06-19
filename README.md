# ChatWithPDF - Summarizer, Translator & QA Bot

Welcome to the PDF Assistant project! This innovative tool is designed to help students and professionals efficiently prepare for exams and understand content. Leveraging advanced machine learning models, PDF Assistant excels in summarization, translation, and question answering, providing an invaluable resource for anyone working with lengthy PDF documents.

## Key Features

- **Summarization**: Quickly generates concise summaries of lengthy PDF documents, helping students study more efficiently.
- **Question Answering**: Provides accurate answers to questions based on the content of the PDF, acting as a smart study assistant.
- **Translation**: Easily translates PDFs into different languages, making it accessible for users worldwide.

## Models Used

The project utilizes the following models from Hugging Face:
- **Summarization**: `facebook/bart-large-cnn`
- **Question Answering**: `distilbert-base-cased-distilled-squad`
- **Translation**: `googletrans`

## Deployment

The PDF Assistant is deployed using the Streamlit framework, ensuring an intuitive and user-friendly experience.

## Installation

To run the PDF Assistant locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/abdullahfirdowsi/ChatWithPDF-Bot.git
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the Streamlit app:
    ```sh
    streamlit run app.py
    ```

## Usage

1. Upload a PDF document through the Streamlit interface.
2. Choose the desired operation: Summarization, Question Answering, or Translation.
3. Interact with the results and refine as needed.

## Acknowledgements

This project uses the following libraries and frameworks:
- [Hugging Face Transformers](https://github.com/huggingface/transformers)
- [Streamlit](https://streamlit.io/)
- [Googletrans](https://py-googletrans.readthedocs.io/en/latest/)

## Contributing

We welcome contributions to the PDF Assistant project! If you have ideas for new features or improvements, please submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, please reach out to me at [abdullahfirdowsi@gmail.com](mailto:abdullahfirdowsi@gmail.com).

Proud of this accomplishment and eager to apply these skills to future projects! 🌟

