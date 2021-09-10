<template>
  <div>
    <svg id="dial_svg"></svg>
  </div>
</template>

<script>
const d3 = require("d3")
const { Note, Scale } = require("@tonaljs/tonal")
console.log(Note,Scale)

export default {
  name: 'InterfaceMovable',

  props:{
    interface_key: String,
    roots: Array
  },

  data: function(){
    return{
      // 'Constants'
      major_scale: [0,2,4,5,7,9,11],

      // Current selection
      current_chord_root: "0",
      current_chord_type: "M",
      current_chord_interval: 3,

      // Dial
      dial_r_outer: 100,
      degree_text: ['I','ii','iii','IV','V','vi','vii°'],

      // Keyboard
      alt: false,
      ctrl: false,
      shift: false,
      s: false
    }
  },

  computed: {
    // Dial
    interface_key_idx: function(){
      return this.roots.indexOf(this.interface_key)
    },

    dial_r_center: function(){
      return this.dial_r_outer/2
    },

    dial_r_degrees: function(){
      return this.dial_r_outer * 1.5
    },

    // Interfacing
    scale_roots: function(){
      return Scale.get(this.interface_key + " major").notes
    }
  },

  methods: {
    // Dial
    outer_text: function(interface_key){
      let scale_notes = Scale.get(interface_key + " major").notes

      for (let i=0; i<3; i++){
        scale_notes[[1,2,5][i]] += "m"
      }
      scale_notes[6] += "dim"
      return scale_notes
    },
    draw_dial(outer_text){
      d3.selectAll('g').remove().exit()
      let g = d3.select("#dial_svg").append('g').attr('class', 'g').attr("transform", "translate("+(this.dial_r_degrees+5)+","+(this.dial_r_degrees+5)+")");
      let This = this
      // Outer Ring & degree (roman numerals)
      for (let i=0; i < outer_text.length; i++){
        let arc = d3.arc()
        .innerRadius(this.dial_r_center)
        .outerRadius(this.dial_r_outer)
        .startAngle(2*i*Math.PI / outer_text.length)
        .endAngle(2*(i+1)*Math.PI / outer_text.length)
    
        g.append("path")
            .attr("d", arc)
            .attr("id", 'outer_path'+i)
            .attr("class", "outer_path")
            .on("click", function(){This.outer_on_click(i)})
            .on("contextmenu", function(e){
              e.preventDefault()
              This.outer_on_click(i)
            })
            .on("mouseover", function(){
                d3.select("#outer_path"+i).classed("outer_path_mouseover",true)
            })
            .on("mouseout", function(){
                d3.select("#outer_path"+i).classed("outer_path_mouseover",false)
            })
        
        g.append("text") 
        .attr("dx", (this.dial_r_outer+this.dial_r_center)/2*Math.cos(2*i*Math.PI / outer_text.length + (-0.5+1/7)*Math.PI))
        .attr("dy", (this.dial_r_outer+this.dial_r_center)/2*Math.sin(2*i*Math.PI / outer_text.length + (-0.5+1/7)*Math.PI))
        .attr("class", "outer_text")
        .attr("id", "outer_text"+i)
        .text(outer_text[i])
        .on("click", function(){This.outer_on_click(i)})
        .on("contextmenu", function(e){
          e.preventDefault()
          This.outer_on_click(i)
        })
        .on("mouseover", function(){
            d3.select("#outer_path"+i).classed("outer_path_mouseover",true)
        })
        .on("mouseout", function(){
            d3.select("#outer_path"+i).classed("outer_path_mouseover",false)
        })

        g.append("text") 
        .attr("dx", (this.dial_r_outer+this.dial_r_degrees)/2*Math.cos(2*i*Math.PI / outer_text.length + (-0.5+1/7)*Math.PI))
        .attr("dy", (this.dial_r_outer+this.dial_r_degrees)/2*Math.sin(2*i*Math.PI / outer_text.length + (-0.5+1/7)*Math.PI))
        .attr("class", "outer_text")
        .text(this.degree_text[i])
    }

    g.append('circle')
        .attr('x',0)
        .attr('y',0)
        .attr('r',this.dial_r_center)
        .attr("class", "center_path")
        

    g.append("text") 
        .attr("class", "center_text")
        .attr("id","center_text")
        .text("")
    },
    get_current_chord_text: function(root){
      if (this.current_chord_interval == 3){
        if (this.current_chord_type == "M"){
          return root
        }
        return root + this.current_chord_type
      }
      if (this.current_chord_type == "D"){
        return root + this.current_chord_interval
      }
      if (this.current_chord_type == "M"){
        return root + "maj" + this.current_chord_interval
      }
      return root + this.current_chord_type + this.current_chord_interval
    },
    update_center_text(text){
      let center_text = d3.select("#center_text")
      center_text.text(text)

      center_text.classed('text_major', false)
      center_text.classed('text_minor', false)
      center_text.classed('text_dom', false)
      if (this.current_chord_type == "M"){
        d3.select("#center_text").classed('text_major', true)
      }
      if (this.current_chord_type == "m"){
        center_text.classed('text_minor', true)
      }
      if (this.current_chord_type == "D"){
        center_text.classed('text_dom', true)
      }
    },
    outer_on_click(i){
      // Interfacing
      this.current_chord_root = (this.major_scale[i] + this.roots.indexOf(this.interface_key)) % 12
      let scale_root_text = this.scale_roots[i]
      if (this.s){
        this.current_chord_root = (this.current_chord_root + 7) % 12
        scale_root_text = this.scale_roots[(i+4)%7]
        if (i == 6){
          if (scale_root_text.length == 2 && scale_root_text.charAt(1) == "b"){
            scale_root_text = scale_root_text.charAt(0)
          }
          else {
            scale_root_text += '#'
          }
        }
        this.current_chord_interval = 7
        this.current_chord_type = "D"
      }
      if (this.alt){
        this.current_chord_interval = 7
        this.current_chord_type = "D"
        if (this.shift){
          this.current_chord_type = "M"
        }
        else if (this.ctrl){
          console.log("CTRL")
          this.current_chord_type = "m"
        }
      }
      else if (this.shift){
        this.current_chord_interval = 3
        this.current_chord_type = "M"
      }
      else if (this.ctrl){
        this.current_chord_interval = 3
        this.current_chord_type = "m"
      }
      else if (! this.s){
        // No key pressed
        this.current_chord_interval = 3
        if ([0,3,4].includes(i)){
          this.current_chord_type = "M"
        }
        else{
          this.current_chord_type = "m"
        }
      }
      this.update_center_text(this.get_current_chord_text(scale_root_text))
      this.$emit('update_current_chord', this.current_chord_root + this.current_chord_type + this.current_chord_interval, this.get_current_chord_text(scale_root_text))

      // Visuals
      for (let i=0; i<7; i++){
        d3.select('#outer_path'+i).classed("outer_path_active",false)
      }
      d3.select('#outer_path'+i).classed("outer_path_active",true)
    },
    keydown_functions(event){
      let key = event.key
      if (key == "Alt"){
        event.preventDefault()
        this.alt = true
      }
      if (key == "Shift"){
        event.preventDefault()
        this.shift = true
      }
      if (key == "Control"){
        event.preventDefault()
        this.ctrl = true
      }
      if (['S','s'].includes(key)){
        event.preventDefault()
        this.s = true
      }
      if (['1','2','3','4','5','6','7'].includes(key)){
        event.preventDefault()
        this.outer_on_click(['1','2','3','4','5','6','7'].indexOf(key))
      }
      if (['!','@','#','$','%','^','&'].includes(key)){
        event.preventDefault()
        this.outer_on_click(['!','@','#','$','%','^','&'].indexOf(key))
      }
      if (['¡','™','£','¢','∞','§','¶'].includes(key)){
        event.preventDefault()
        this.outer_on_click(['¡','™','£','¢','∞','§','¶'].indexOf(key))
      }
      if (['⁄','€','‹','›','ﬁ','ﬂ','‡'].includes(key)){
        event.preventDefault()
        this.outer_on_click(['⁄','€','‹','›','ﬁ','ﬂ','‡'].indexOf(key))
      }
    },
    keyup_functions(event){
      let key = event.key
      if (key == "Alt"){
        event.preventDefault()
        this.alt = false
      }
      if (key == "Shift"){
        event.preventDefault()
        this.shift = false
      }
      if (key == "Control"){
        event.preventDefault()
        this.ctrl = false
      }
      if (['S','s'].includes(key)){
        event.preventDefault()
        this.s = false
      }
    }
  },

  mounted(){
    this.draw_dial(this.outer_text(this.interface_key))
    
    // Handle keyboard inputs
    document.addEventListener('keydown', this.keydown_functions)
    document.addEventListener('keyup', this.keyup_functions)
  },

  beforeUnmount(){
    document.removeEventListener('keydown', this.keydown_functions)
    document.removeEventListener('keyup', this.keyup_functions)
  }

}
</script>

<style>
/* Dial /////////////////////////////////////*/
#dial_svg{
    width: 400px;
    height: 400px;
}

.outer_path{
    stroke: black;
    fill: white;
}

.outer_text{
    stroke: black;
    fill: black;
    stroke-width: 0;
    font-size: 15px;
    user-select: none;
    dominant-baseline: middle;
    text-anchor: middle;
}

.outer_path_mouseover{
    fill: #80b8f5;
}

.outer_path_active{
    fill: #347dff;
}

.center_path{
    stroke: black;
    fill: white;
}

.center_text{
    stroke-width: 0;
    font-size: 25px;
    user-select: none;
    dominant-baseline: middle;
    text-anchor: middle;
}

.text_major{
    fill:#3b9aff;
}

.text_minor{
    fill:#0069da;
}
.text_dom{
  fill: #ff9797;
}
</style>
