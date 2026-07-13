// kenya_locations.js

const data = {
    "Nairobi": {
        "Westlands": ["Parklands", "Kitisuru", "Karura"],
        "Dagoretti": ["Mutu-ini", "Ngando", "Riruta"],
        "Embakasi": ["Utawala", "Umoja", "Kariobangi"]
    },

    "Kiambu": {
        "Gatundu North": ["Gituamba", "Gatukuyu"],
        "Thika": ["Township", "Kamenu", "Hospital"],
        "Ruiru": ["Gitothua", "Biashara", "Kahawa Sukari"]
    },

    "Kisumu": {
        "Kisumu Central": ["Market", "Shauri Moyo", "Kaloleni"],
        "Kisumu East": ["Manyatta", "Nyalenda"],
        "Kisumu West": ["Kondele", "Ojolla"]
    }
};

// DOM elements
const countySelect = document.getElementById("county");
const subCountySelect = document.getElementById("sub_county");
const wardSelect = document.getElementById("ward");

// 1. Load counties
function loadCounties() {
    countySelect.innerHTML = '<option value="">Select County</option>';

    Object.keys(data).forEach(county => {
        let option = document.createElement("option");
        option.value = county;
        option.textContent = county;
        countySelect.appendChild(option);
    });
}

// 2. Load sub-counties based on county
countySelect.addEventListener("change", function () {
    const selectedCounty = this.value;

    subCountySelect.innerHTML = '<option value="">Select Sub-county</option>';
    wardSelect.innerHTML = '<option value="">Select Ward</option>';

    if (selectedCounty && data[selectedCounty]) {
        Object.keys(data[selectedCounty]).forEach(sub => {
            let option = document.createElement("option");
            option.value = sub;
            option.textContent = sub;
            subCountySelect.appendChild(option);
        });
    }
});

// 3. Load wards based on sub-county
subCountySelect.addEventListener("change", function () {
    const county = countySelect.value;
    const sub = this.value;

    wardSelect.innerHTML = '<option value="">Select Ward</option>';

    if (county && sub && data[county][sub]) {
        data[county][sub].forEach(ward => {
            let option = document.createElement("option");
            option.value = ward;
            option.textContent = ward;
            wardSelect.appendChild(option);
        });
    }
});

// Initialize
loadCounties();