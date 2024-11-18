// Sample Data with Image URLs, Coordinates, and City (replace with actual URLs and data)
const images = [
    { id: 1, date: '2023-11-01', type: 'wildfire', intensity: 'high', description: 'High-intensity wildfire in forest area', src: 'https://buffer.com/library/content/images/size/w1200/2023/10/free-images.jpg', longitude: -120.5, latitude: 38.5, city: 'Baku' },
    { id: 2, date: '2023-11-05', type: 'fire', intensity: 'medium', description: 'Medium-intensity fire near urban area', src: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Sunflower_from_Silesia2.jpg/1280px-Sunflower_from_Silesia2.jpg', longitude: -119.2, latitude: 36.8, city: 'Ganja' },
    { id: 3, date: '2023-11-10', type: 'wildfire', intensity: 'low', description: 'Low-intensity wildfire in grassland', src: 'https://plus.unsplash.com/premium_photo-1666672388644-2d99f3feb9f1?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8anBnfGVufDB8fDB8fHww', longitude: -121.3, latitude: 37.7, city: 'Sumqayit' },
    // Add more images as needed
  ];
  
  function displayImages(imageList) {
    const gallery = document.getElementById('image-gallery');
    gallery.innerHTML = ''; // Clear previous images
  
    imageList.forEach(image => {
      const imageItem = document.createElement('div');
      imageItem.className = 'image-item';
  
      const img = document.createElement('img');
      img.src = image.src;  // Use the image URL from 'src' in the data
      img.alt = image.description;
  
      const info = document.createElement('div');
      info.className = 'info';
      info.textContent = `${image.date} - ${image.type} - ${image.intensity} - ${image.city} (${image.longitude}, ${image.latitude})`;
  
      imageItem.appendChild(img);
      imageItem.appendChild(info);
      gallery.appendChild(imageItem);
    });
  }
  
  // Initial display of all images
  displayImages(images);
  
  function filterImages() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const type = document.getElementById('type').value;
    const intensity = document.getElementById('intensity').value;
    const city = document.getElementById('city').value;
    const minLongitude = parseFloat(document.getElementById('min-longitude').value);
    const maxLongitude = parseFloat(document.getElementById('max-longitude').value);
    const minLatitude = parseFloat(document.getElementById('min-latitude').value);
    const maxLatitude = parseFloat(document.getElementById('max-latitude').value);
  
    const filteredImages = images.filter(image => {
      const dateMatch = (!startDate || new Date(image.date) >= new Date(startDate)) && 
                        (!endDate || new Date(image.date) <= new Date(endDate));
      const typeMatch = type === 'all' || image.type === type;
      const intensityMatch = intensity === 'all' || image.intensity === intensity;
      const cityMatch = city === 'all' || image.city === city;
      const longitudeMatch = (isNaN(minLongitude) || image.longitude >= minLongitude) && 
                             (isNaN(maxLongitude) || image.longitude <= maxLongitude);
      const latitudeMatch = (isNaN(minLatitude) || image.latitude >= minLatitude) && 
                            (isNaN(maxLatitude) || image.latitude <= maxLatitude);
  
      return dateMatch && typeMatch && intensityMatch && cityMatch && longitudeMatch && latitudeMatch;
    });
  
    displayImages(filteredImages);
  }
  