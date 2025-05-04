/**
 * CarZone E-commerce - Main JavaScript File
 * Refactored for better organization and maintainability
 */

// Price Range Slider Initialization
const initPriceRangeSlider = () => {
	$('#sl2').slider();
  };
  
  // RGB Color Changer (if still needed)
  const initRGBColorChanger = () => {
	const RGBChange = () => {
	  $('#RGB').css('background', `rgb(${r.getValue()},${g.getValue()},${b.getValue()})`);
	};
	// Note: Ensure r, g, b variables are defined elsewhere or this won't work
  };
  
  // Scroll to Top Button Configuration
  const initScrollToTop = () => {
	$.scrollUp({
	  scrollName: 'scrollUp',
	  scrollDistance: 300,
	  scrollFrom: 'top',
	  scrollSpeed: 300,
	  easingType: 'linear',
	  animation: 'fade',
	  animationSpeed: 200,
	  scrollTrigger: false,
	  scrollText: '<i class="fas fa-angle-up"></i>', // Updated to Font Awesome 5+ class
	  scrollTitle: false,
	  scrollImg: false,
	  activeOverlay: false,
	  zIndex: 2147483647
	});
  };
  
  // Document Ready Handler
  $(document).ready(() => {
	// Initialize all components
	initPriceRangeSlider();
	initScrollToTop();
	
	// Uncomment if RGB functionality is needed
	// initRGBColorChanger();
  });
  
  // Optional: Add modern event listeners for better performance
  const setupEventListeners = () => {
	// Example: Handle product filter changes
	$(document).on('change', '.product-filter', function() {
	  // Add filter logic here
	});
	
	// Example: Cart quantity adjustments
	$(document).on('click', '.quantity-btn', function() {
	  // Add quantity adjustment logic here
	});
  };
  
  // Initialize event listeners when DOM is ready
  $(document).ready(setupEventListeners);