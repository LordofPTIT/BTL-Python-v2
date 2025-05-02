let forest;

     // Tải mô hình từ backend
     fetch('http://localhost:5000/model')
         .then(response => response.json())
         .then(data => {
             forest = data;
         })
         .catch(error => console.error('Error fetching model:', error));

     // Hàm dự đoán
     function predict(forest, X) {
         const predictions = forest.map(tree => predictTree(tree, X));
         const sum = predictions.reduce((acc, val) => acc + val, 0);
         return sum / predictions.length > 0.5 ? 1 : 0;
     }

     function predictTree(tree, X) {
         if ('value' in tree) {
             return tree.value[0][1];  // Giả sử phân loại nhị phân
         } else {
             const feature = tree.feature;
             const threshold = tree.threshold;
             if (X[feature] <= threshold) {
                 return predictTree(tree.left, X);
             } else {
                 return predictTree(tree.right, X);
             }
         }
     }

     // Lắng nghe tin nhắn từ content script
     chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
         if (message.type === 'classify') {
             const X = message.features;
             if (forest) {
                 const prediction = predict(forest, X);
                 sendResponse({prediction: prediction});
             } else {
                 sendResponse({error: 'Model not loaded'});
             }
         }
     });