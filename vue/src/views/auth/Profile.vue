<template>
  <div>
    <a-page-header
      style="border: 1px solid rgb(235, 237, 240); margin-bottom: 2rem"
      title="用户信息"
    />
    <a-form-model :model="form" :label-col="labelCol" :wrapper-col="wrapperCol">
      <a-form-model-item label="昵称">
        <a-input v-model="form.nickname" disabled />
      </a-form-model-item>
      <a-form-model-item label="密码">
        <a-input v-model="form.password" type="password" disabled/>
      </a-form-model-item>
      <a-form-model-item label="注册时间">
        {{ form.date1 }}
      </a-form-model-item>
      <a-form-model-item label="账号（手机）">
        {{ form.phone }}
      </a-form-model-item>
      <a-form-model-item label="用户资产">
        {{ form.restAsset }} ￥
        <el-button
          type="primary"
          @click="showBuy=true"
          style="margin-right: 2rem"
          >充值</el-button
        >
      </a-form-model-item>

      <a-form-model-item label="身份权限">
        {{ form.role }}
      </a-form-model-item>
    </a-form-model>

       <el-dialog :visible.sync="showBuy" width=20%>
      <el-form label-width="100px" >
        <el-form-item label="充值金额：">
          <el-input v-model="input" style="width:50%" clearable placeholder="请输入"></el-input>
          <el-button type="primary" @click="pay">支付</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { formatDate } from '../../utils/common.js'
export default {
  name: "Profile",
  props: {
    user_info: {
      type: Object,
    },
  },
  data() {
    return {
      input:'',
      showBuy:false,
      labelCol: { span: 4 },
      wrapperCol: { span: 14 },
      form: {
        nickname: this.user_info.nickname,
        phone: this.user_info.phone,
        date1: formatDate(this.user_info.create_time),
        password: this.user_info.password,
        role: this.formatRole(this.user_info.role),
        restAsset: this.formatRestAsset(this.user_info.rest_asset),
      },
    };
  },
  mounted() {
  },
  methods: {
      pay(){
       var param = {
        money: this.input,
        id: this.user_info.id
      }
        this.$alipay_api.recharge(param).then((res) => {
          if (res.code==200){
            this.$alipay_api.addasset(param).then((res) => {
                  if (res.code==200){
                    console.log(res)
                    this.$message.success("充值成功！")
                  }
              })
            window.location.assign(res.data)
          }
      })


      },


      /**
       * 字段转换用户角色名称
       */
      formatRole(role) {
        if (role == 'user') {
            return '普通用户'
        }
        if (role == 'admin') {
            return '超级管理员'
        }
      },

      /**
       * 若未返回用户资产，设置资产为0
       */
      formatRestAsset(restAsset) {
          if (restAsset == undefined) {
              return 0
          }
          return restAsset
      }
  }
};
</script>