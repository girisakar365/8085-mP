export const parseDocumentation = (docString) => {
  const lines = docString.split('\n');
  let currentSection = 'description';
  
  const result = {
    description: '',
    args: [],
    raises: [],
    notes: [],
    example: []
  };
  
  for (const line of lines) {
    const trimmedLine = line.trim();
    
    if (line.startsWith('Args:')) {
      currentSection = 'args';
      continue;
    } else if (line.startsWith('Raises:')) {
      currentSection = 'raises';
      continue;
    } else if (line.startsWith('Notes:')) {
      currentSection = 'notes';
      continue;
    } else if (line.startsWith('Example:')) {
      currentSection = 'example';
      continue;
    }
    
    if (trimmedLine) {
      if (currentSection === 'raises' && trimmedLine.startsWith('-')) {
        result.raises.push(trimmedLine.substring(2).trim());
      } else if (currentSection === 'description') {
        result.description += trimmedLine + ' ';
      } else if (currentSection === 'args') {
        result.args.push(line); 
      } else if (currentSection === 'notes') {
        result.notes.push(trimmedLine);
      } else if (currentSection === 'example') {
        result.example.push(line);
      }
    }
  }
  
  return result;
};
