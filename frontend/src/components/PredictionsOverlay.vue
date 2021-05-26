<script>
import { Overlay } from 'trading-vue-js'

export default {
  name: 'PredictionsOverlay',
  mixins: [Overlay],
  methods: {
    draw(ctx) {
      console.log('tyt')
      let layout = this.$props.layout; // Layout object (see API BOOK)
      const c = {
          x: layout.width / 2,
          y: layout.height / 2
      }
      
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = 'black';

      // let p1 = 1621857600000;
      // let p2 = 71;

      ctx.fillStyle = '#bfff00'
      ctx.beginPath()
      // let x = layout.t2screen(p1); // x - Mapping
      // let y = layout.$2screen(p2); // y - Mapping
      ctx.arc(c.x, c.y, 50, 0, Math.PI * 2, true) // Trade point
      ctx.fill()
      ctx.stroke()
      

      // for (var p of this.$props.graph.data) {
      //     ctx.fillStyle = p[1] ? '#bfff00' : '#ec4662'
      //     ctx.beginPath()
      //     let x = layout.t2screen(p[0]) // x - Mapping
      //     let y = layout.$2screen(p[2]) // y - Mapping
      //     ctx.arc(x, y, 5.5, 0, Math.PI * 2, true) // Trade point
      //     ctx.fill()  
      //     ctx.stroke()
      // }
      
    },
    use_for() {
      return ['PredictionsOverlay'] 
    }
  }
}
</script>
