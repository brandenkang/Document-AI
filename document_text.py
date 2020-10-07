# export GOOGLE_APPLICATION_CREDENTIALS="/Users/BrandenKang/Document-AI/document-ai-project-b7464d94d7f7.json"
# document-ai-project-291706
# gs://analysis_report_samples/

from google.cloud import documentai_v1beta2 as documentai

def main(project_id='document-ai-project-291706',
        input_uri='gs://analysis_report_samples/sample_ocr_1.pdf'):
        #  input_uri='gs://cloud-samples-data/documentai/invoice.pdf'):

    """Process a single document with the Document AI API, including
    text extraction and entity extraction."""

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type='application/pdf')

    # Location can be 'us' or 'eu'
    parent = 'projects/{}/locations/us'.format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config)

    document = client.process_document(request=request)

    file_= open('output.text','w')
    # All text extracted from the document
    print('Document Text: {}'.format(document.text))
    file_.write('Document Text: {}'.format(document.text))
    def _get_text(el):
        """Convert text offset indexes into text snippets.
        """
        response = ''
        # If a text segment spans several lines, it will
        # be stored in different text segments.
        for segment in el.text_anchor.text_segments:
            start_index = segment.start_index
            end_index = segment.end_index
            response += document.text[start_index:end_index]
        return response

    for entity in document.entities:
        # print('Entity type: {}'.format(entity.type))
        print('Text: {}'.format(_get_text(entity)))
        file_.write('Text: {}'.format(_get_text(entity)))
        print('Mention text: {}\n'.format(entity.mention_text))
        file_.write('Mention text: {}\n'.format(entity.mention_text))


    file_.close()


main()