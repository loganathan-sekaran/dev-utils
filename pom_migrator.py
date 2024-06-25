from xml.etree import ElementTree as ET
from text_changes import kernel_bom_dependency_xml

# Parse the dependency XML string
dependency_element = ET.fromstring(kernel_bom_dependency_xml)

ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")
ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")

def addKernelBomToDependencyMgnt(pomFilePath):
    print("Adding kernel-bom dependency to: " + pomFilePath)
    # Load the POM file
    pom_tree = ET.parse(pomFilePath)
    pom_root = pom_tree.getroot()

    # Find the dependencyManagement section
    dependency_management = pom_root.find('{http://maven.apache.org/POM/4.0.0}dependencyManagement')
    if dependency_management is None:
        # Create dependencyManagement section if it doesn't exist
        dependency_management = ET.SubElement(pom_root, 'dependencyManagement')
        dependencies = ET.SubElement(dependency_management, 'dependencies')
    else:
        # Find the dependencies section within dependencyManagement
        dependencies = dependency_management.find('{http://maven.apache.org/POM/4.0.0}dependencies')

    for child in dependency_element:
        child.tag = child.tag.split('}', 1)[-1]
    
    # Add the new dependency
    dependencies.append(dependency_element)

    # Save the modified POM file
    pom_tree.write(pomFilePath, xml_declaration=True, encoding='utf-8')

    # Print a success message
    print("The kernel-bom dependency has been successfully added to the dependencyManagement section of the POM file.")
