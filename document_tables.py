from google.cloud import documentai_v1beta2 as documentai


def parse_table(project_id='document-ai-project-291706',
                input_uri='gs://analysis_report_samples/sample_ocr_1.pdf'):

    client = documentai.DocumentUnderstandingServiceClient()

    gcs_source = documentai.types.GcsSource(uri=input_uri)

    # mime_type can be application/pdf, image/tiff,
    # and image/gif, or application/json
    input_config = documentai.types.InputConfig(
        gcs_source=gcs_source, mime_type='application/pdf')

    # Improve table parsing results by providing bounding boxes
    # specifying where the box appears in the document (optional)
    table_bound_hints = [
        documentai.types.TableBoundHint(
            page_number=1,
            bounding_box=documentai.types.BoundingPoly(
                # Define a polygon around tables to detect
                # Each vertice coordinate must be a number between 0 and 1
                normalized_vertices=[
                    # Top left
                    documentai.types.geometry.NormalizedVertex(
                        x=0,
                        y=0
                    ),
                    # Top right
                    documentai.types.geometry.NormalizedVertex(
                        x=1,
                        y=0
                    ),
                    # Bottom right
                    documentai.types.geometry.NormalizedVertex(
                        x=1,
                        y=1
                    ),
                    # Bottom left
                    documentai.types.geometry.NormalizedVertex(
                        x=0,
                        y=1
                    )
                ]
            )
        )
    ]

    # Setting enabled=True enables form extraction
    table_extraction_params = documentai.types.TableExtractionParams(
        enabled=True, table_bound_hints=table_bound_hints)

    # Location can be 'us' or 'eu'
    parent = 'projects/{}/locations/us'.format(project_id)
    request = documentai.types.ProcessDocumentRequest(
        parent=parent,
        input_config=input_config,
        table_extraction_params=table_extraction_params)

    document = client.process_document(request=request)

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

    file_= open('output_table_sample_1.text','w')
    for page in document.pages:
        print('Page number: {}'.format(page.page_number))
        file_.write('Page number: {}'.format(page.page_number))
        for table_num, table in enumerate(page.tables):
            print('Table {}: '.format(table_num))
            file_.write('Table {}: '.format(table_num))
            for row_num, row in enumerate(table.header_rows):
                cells = '\t'.join(
                    [_get_text(cell.layout) for cell in row.cells])
                print('Header Row {}: {}'.format(row_num, cells))
                file_.write('Header Row {}: {}'.format(row_num, cells))
            for row_num, row in enumerate(table.body_rows):
                cells = '\t'.join(
                    [_get_text(cell.layout) for cell in row.cells])
                print('Row {}: {}'.format(row_num, cells))
                file_.write('Row {}: {}'.format(row_num, cells))
    file_.close()

parse_table()