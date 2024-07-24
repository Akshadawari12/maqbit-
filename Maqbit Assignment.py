import scribus
import xml.etree.ElementTree as ET

def import_articles_from_xml(xml_file):

    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Validate root element
        if root.tag != 'articles':
            raise ValueError("Invalid XML format: Root element is not 'articles'")

        # Initialize coordinates for placing text frames
        x, y = 20, 20  # starting coordinates
        title_height, description_height = 30, 50  # heights for the text frames
        spacing = 20  # space between frames

        for articles in root.findall('article'):
            title = articles.find('title').text
            description = articles.find('description').text

            # Create and style title text frame
            title_frame = scribus.createText(x, y, 500, title_height)
            scribus.setText(title, title_frame)
            scribus.setFont("Arial Bold", title_frame)
            scribus.setFontSize(14, title_frame)

            # Adjust y position for the description text frame
            y += title_height + spacing

            # Create and style description text frame
            desc_frame = scribus.createText(x, y, 500, description_height)
            scribus.setText(description, desc_frame)
            scribus.setFont("Arial", desc_frame)
            scribus.setFontSize(12, desc_frame)

            # Adjust y position for the next article
            y += description_height + spacing

        scribus.setRedraw(True)
        scribus.redrawAll()
        scribus.statusMessage("Articles imported successfully.")

    except FileNotFoundError:
        scribus.messageBox("Error", "File {xml_file} not found.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    except ET.ParseError:
        scribus.messageBox("Error", "Failed to parse the XML file {xml_file}.", scribus.ICON_WARNING,
                           scribus.BUTTON_OK)
    except ValueError as e:
        scribus.messageBox("Error", str(e), scribus.ICON_WARNING, scribus.BUTTON_OK)
    except Exception as e:
        scribus.messageBox("Error", "An unexpected error occurred: {str(e)}", scribus.ICON_WARNING, scribus.BUTTON_OK)


if __name__ == "__main__":
    if not scribus.haveDoc():
        scribus.messageBox("Error","No document open. Please open a document first",icon=scribus.ICON_WARNING, buttons=scribus.BUTTON_OK)
    else:
        import_articles_from_xml('example.xml')
