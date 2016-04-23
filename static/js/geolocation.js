window.Geolocation = {
    latitude: $('[name="latitude"]'),
    longitude: $('[name="longitude"]'),
    init: function() {
        this.getLocation();
    },
    getLocation: function() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(this.fillPosition);
        }
    },
    fillPosition: function(position) {
        window.Geolocation.latitude.val(position.coords.latitude);
        window.Geolocation.longitude.val(position.coords.longitude);
    }
};

window.Geolocation.init();