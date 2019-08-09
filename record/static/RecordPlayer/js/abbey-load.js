/*
 * load.js
 * A music asset loader by Stuart Memo 
 */

(function (window, undefined) {
    window.AudioContext = window.AudioContext||window.webkitAudioContext;

    var filesLoaded = 0,
        numberOfFiles = 0,
        context = new AudioContext(),
        buffers = [];

    var Load = function (files, callback, onProgress) {
        this.files = files || {}; 
        filesLoaded = 0;
        numberOfFiles = 0;
        loadFiles(this.files, callback, onProgress);
    };

    Load.size = function(obj) {
        var size = 0;

        for (var key in obj) {
            
            if (obj.hasOwnProperty(key)){
                size++;
            }
        }
        return size;
    };

    var loadFile = function (fileKey, file, returnObj, callback, onProgress) {
        var request = new XMLHttpRequest();

        request.open('GET', file[fileKey], true);
        request.responseType = 'arraybuffer';

        request.onload = function () {        	
            filesLoaded++;
            context.decodeAudioData(request.response, function (decodedBuffer) {
                returnObj[fileKey] = decodedBuffer;
                if( typeof onProgress === 'function' ) {
                    onProgress(Load.size(returnObj)*100/numberOfFiles);
                }
                if (Load.size(returnObj) === numberOfFiles) {
                    callback(returnObj);
                }
            });
        };

        request.send();
    };

    var loadFiles = function (files, callback, onProgress) {
        var returnObj = {};

        files.forEach(function (file, index) {
		    
            numberOfFiles = Load.size(file);

            for (var key in file) {
                if (file.hasOwnProperty(key)) {
                    loadFile(key, file, returnObj, callback, onProgress);
                }
            }

        });
    };

    window.Load = Load;
})(window);