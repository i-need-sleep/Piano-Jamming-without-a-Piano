<template>
  <div>


  <!-- Current chord display -->
    <p>Current chord:</p>
    <p id=current_chord_text v-bind:class="{'text_major':current_chord_type=='M', 'text_minor':current_chord_type=='m', 'text_dom':current_chord_type=='D'}"> {{ current_chord_text }} </p>


  <!-- Root selector -->
    <table id="root_table" class="table table-bordered table-fixed">
      <tbody>
        <tr>
          <td v-for="i in 12" v-bind:key="i" v-bind:id="'root_'+i" 
            v-on:click="root_on_click(i-1, $event)" 
            v-on:contextmenu.prevent="root_on_rightclick(i-1, $event)"
            v-on:click.middle="root_on_middleclick(i-1, $event)" 
            v-bind:class="{'root_cell':true, 
                            'root_black':[1,3,6,8,10].includes(i-1),
                            'major':current_chord_type=='M'&&current_chord_root==i-1, 
                            'minor':current_chord_type=='m'&&current_chord_root==i-1,
                            'dom':current_chord_type=='D'&&current_chord_root==i-1
                            }" >
            {{roots[i-1]}}
          </td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
export default {
  name: 'InterfaceFixed',

  data: function(){
    return{
      // 'Constants'
      roots: ['C','C#','D','D#','E',"F",'F#','G','G#','A','A#','B'],

      // Current selection
      current_chord_root: "0",
      current_chord_type: "M",
      current_chord_interval: 3
    }
  },

  computed: {
    current_chord_text: function(){
      if (this.current_chord_interval == 3){
        if (this.current_chord_type == "M"){
          return this.roots[this.current_chord_root]
        }
        return this.roots[this.current_chord_root] + this.current_chord_type
      }
      if (this.current_chord_type == "D"){
        return this.roots[this.current_chord_root] + this.current_chord_interval
      }
      if (this.current_chord_type == "M"){
        return this.roots[this.current_chord_root] + "maj" + this.current_chord_interval
      }
      return this.roots[this.current_chord_root] + this.current_chord_type + this.current_chord_interval
    }
  },

  methods: {
    root_on_click(root_idx, event){
      if (event.ctrlKey){
        this.root_on_rightclick(root_idx, event)
        return
      }
      this.current_chord_root = root_idx
      this.current_chord_type = "M"
      if (event.altKey){
        this.current_chord_interval = 7
      }
      else if (event.shiftKey && event.movementX != undefined){
        this.current_chord_type = "D"
        this.current_chord_interval = 7
      }
      else{
        this.current_chord_interval = 3
      }
      this.$emit('update_current_chord', this.current_chord_root + this.current_chord_type + this.current_chord_interval, this.current_chord_text)
    },
    root_on_rightclick(root_idx, event){
      this.current_chord_root = root_idx
      this.current_chord_type = "m"
      this.current_chord_interval = 3
      if (event.altKey){
        this.current_chord_interval = 7
      }
      else{
        this.current_chord_interval = 3
      }
      this.$emit('update_current_chord', this.current_chord_root + this.current_chord_type + this.current_chord_interval, this.current_chord_text)
    },
    root_on_middleclick(root_idx){
      this.current_chord_root = root_idx
      this.current_chord_type = "D"
      this.current_chord_interval = 7
      this.$emit('update_current_chord', this.current_chord_root + this.current_chord_type + this.current_chord_interval, this.current_chord_text)
    },
    keyboard_functions(event){ 
      let key = event.key
      // Major
      if (['!','@','#','$','%','^','&','*','(',')','_','+'].includes(key)){
          event.preventDefault()
          let idx = ['!','@','#','$','%','^','&','*','(',')','_','+'].indexOf(key)
          this.root_on_click(idx, event)
      }
      else if (['⁄','€','‹','›','ﬁ','ﬂ','‡','°','·','—','±'].includes(key)){
          event.preventDefault()
          let idx = ['⁄','€','‹','›','ﬁ','ﬂ','‡','°','·','—','±'].indexOf(key)
          this.root_on_click(idx, event)
      }
      // Minor
      else if (['1','2','3','4','5','6','7','8','9','0','-','='].includes(key) && event.ctrlKey){
          event.preventDefault()
          let idx = ['1','2','3','4','5','6','7','8','9','0','-','='].indexOf(key)
          this.root_on_rightclick(idx, event)
      }
      // Dominant
      else if (['1','2','3','4','5','6','7','8','9','0','-','='].includes(key) && event.altKey){
          event.preventDefault()
          let idx = ['1','2','3','4','5','6','7','8','9','0','-','='].indexOf(key)
          this.root_on_middleclick(idx, event)
      }
      else if (['¡','™','£','¢','∞','§','¶','•','ª','º','–','≠'].includes(key)){
          event.preventDefault()
          let idx = ['¡','™','£','¢','∞','§','¶','•','ª','º','–','≠'].indexOf(key)
          this.root_on_middleclick(idx, event)
      }
    }
  },

  mounted(){
    // Handle keyboard inputs
    document.addEventListener('keydown', this.keyboard_functions)
  },
  
  beforeUnmount() {
    document.removeEventListener('keydown', this.keyboard_functions);
  }

}
</script>

<style scoped>

/* Current chord text ////////////////////////////////////////////////////////////////////*/
#current_chord_text{
    font-size: 100px;
    text-anchor: middle;
}

.text_major{
    color:#2990ff;
}

.text_minor{
    color:#295bff;
}
.text_dom{
  color: #ff9797;
}


/* Root Table /////////////////////////////////////////////////////////////////////////////*/
#root_table{
    width: 720px !important;
}

.root_cell{
    width: 60px;
    text-anchor: middle;
    text-align: center;
    vertical-align: middle !important;
    -webkit-user-select: none;         
    -moz-user-select: none; 
    -ms-user-select: none; 
    user-select: none; 
}
.root_cell:hover{
    background-color: #80b8f5;
}

.root_black{
    background-color: #aaaaaa;
}

.major{
    background-color: #29b1ff;
}
.major:hover{
    background-color: #00a2ff;
}

.minor{
    background-color: #436efc;
}
.minor:hover{
    background-color: #295bff;
}

.dom{
    background-color: #ff9797;
}
.dom:hover{
    background-color: #ff7575;
}

</style>
