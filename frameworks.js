const FRAMEWORKS = (() => {
  const request = new XMLHttpRequest();
  request.open('GET', './frameworks.json', false);
  request.send();
  if(request.status && request.status !== 200) throw new Error('Could not load the analysis frameworks.');
  return JSON.parse(request.responseText);
})();
