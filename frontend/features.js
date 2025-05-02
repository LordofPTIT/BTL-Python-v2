// Trích xuất đặc trưng từ trang
     function extractFeatures() {
         const url = window.location.href;
         const urlLength = url.length;
         const hasIp = /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/.test(url) ? 1 : 0;
         // Thêm các đặc trưng khác theo tập dữ liệu
         return [urlLength, hasIp];
     }

     // Gửi đặc trưng đến background để phân loại
     const features = extractFeatures();
     chrome.runtime.sendMessage({type: 'classify', features: features}, response => {
         if (response.prediction === 1) {
             alert('Cảnh báo: Trang web này có thể là lừa đảo!');
         }
     });