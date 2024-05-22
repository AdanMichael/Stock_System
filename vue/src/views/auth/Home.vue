<template>
  <div>
      <div class="block" >
    <el-carousel trigger="click" height="600px" arrow="always">
     <el-carousel-item v-for="item in imgList" :key="item.id">
                     <img :src="item.idView" class="image" style="object-fit: scale-down;width: 100%;height: 100%">
       </el-carousel-item>
    </el-carousel>
  </div>

   </div>
</template>


<script>
export default {
    name: 'Home',
    data(){
        return {
            imgList: [
                {id:0,idView:require('../../assets/img/1.jpg')},
                {id:1,idView:require('../../assets/img/2.jpg')},
                {id:2,idView:require('../../assets/img/3.jpg')},
                {id:3,idView:require('../../assets/img/4.jpg')},
                {id:4,idView:require('../../assets/img/5.jpg')}
            ]
        };
        },
    methods: {
    }
}
</script>

<style>

</style>
