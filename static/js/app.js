
function populate() {
    /* data route */
    var url = "/names";

    //var options = Plotly.d3.select("#selDataset").append("select");

    var dropDown = document.getElementById("selDataset");

    Plotly.d3.json(url, function(error,sample_names){
        if (error) return console.log("error");
        for (var i = 0; i < sample_names.length; i++){
            var option1 = document.createElement("option");
            option1.text = sample_names[i];
            option1.value = sample_names[i];
            dropDown.append(option1);
        }
    });
    // Plotly.d3.json(url,function(error,sample_names){
    //     if (error) return console.log(error);
    //     console.log(sample_names);

    //     options.select("select").selectALL("option")
    //     .data(sample_names)
    //     .enter()
    //     .append("option")
    //     .text("something");

    //     console.log(options)

    // })
};

function optionChanged(sample1){
    url = "/samples/"+sample1;

    var PIE = document.getElementById("pie");

    Plotly.d3.json(url, function(error,sample_data){
        if (error) return console.log("error");

        sampleOTU = sample_data.otu_id.slice(0,10);
        sampleVALUES = sample_data.sample_values.slice(0,10);

        var data = [{
            values: sampleVALUES,
            labels: sampleOTU,
            type: "pie"
          }];
        
          var layout = {
            height: 1200,
            width: 1600
          };
        
          Plotly.restyle(PIE, "values", [sampleVALUES])
         // Plotly.restyle(PIE,"labels",[sampleOTU]);

         updatePlot(sampleOTU,sampleVALUES);


        });

}

function init(){
    populate();

    initSample = "BB_940";

    url = "/samples/"+initSample;

    Plotly.d3.json(url, function(error,sample_data){
        if (error) return console.log("error");

        sampleOTU = sample_data.otu_id.slice(0,10);
        sampleVALUES = sample_data.sample_values.slice(0,10);

        all_OTU = sample_data.otu_id;
        all_VALUE = sample_data.sample_values;

        console.log(all_VALUE)

        var data = [{
            values: sampleVALUES,
            labels: sampleOTU,
            type: "pie"
          }];
        
        var layout = {
            height: 1200,
            width: 1600
          };

        var trace1 = {
            x: all_OTU,
            y: all_VALUE,
            mode: "markers",
            text: all_OTU.map(a => a),
            marker: {
            size: all_VALUE.map(a => a*1.2)
            }
            
        };
            

         

        var layoutBubble = {
            title: initSample,
            showlegend: false,
            height: 600,
            width: 1200
          };

        var dataBubble = [trace1];

        console.log(dataBubble)


        
          Plotly.plot("pie", data, layout);

          Plotly.newPlot('bubble',dataBubble,layoutBubble);

          updatePlot(sampleOTU,sampleVALUES, all_OTU, all_VALUE);

        
    });

    
};

function updatePlot(sampleOTU,sampleVALUES,all_OTU,all_VALUE){
    url = "/otu";
    bacteriaLabel = [];
    bacteriaLabelALL = [];
    var PIE = document.getElementById("pie");
    var BUBBLE = document.getElementById("bubble");
    Plotly.d3.json(url,function(error,otu_data){
        for (var i = 0; i < sampleOTU.length; i++){
            bacteriaLabel.push(otu_data[sampleOTU[i]])
        }

        for (var j = 0; i < all_OTU.length; i++){
            bacteriaLabelALL.push(otu_data[all_OTU[i]])
        }
          
          Plotly.restyle(PIE,"labels",[bacteriaLabel]);
         // Plotly.restyle(BUBBLE, "text",[bacteriaLabelALL]);
    

    })



}


init();