<template>
  <div>
    <a-row type="flex">
    <a-col flex="40%" style="margin-left:5rem;">
        <!-- 搜索自选股对话框 -->
        <div>
          <span>用户ID或名称或手机号：</span>
          <a-auto-complete
            v-model="userValue"
            style="width: 50%"
            placeholder="请输入"
            @search="onSearchUser"
          /><a-spin :spinning="searchLoading"/>
          </div>
      </a-col>

    <a-col flex="auto">
        <a-button type="primary" @click="btnSearchUser">
          搜索
        </a-button>
      </a-col>

      <a-col flex="auto">
        <a-button type="primary" @click="addUser">
         添加用户
        </a-button>
      </a-col>



       </a-row>
   <!-- 表格数据展示 -->
    <a-table
      :columns="columns"
      :data-source="data"
      :pagination="pagination"
      :loading="loading"
      @change="handleTableChange"
      style="margin-top:2rem;"
    >
      <!-- 公司详情页面 -->
      <template slot="id" slot-scope="text">
        {{ text }}
      </template>
      <template slot="mc" slot-scope="text, row">
        {{ text }}
      </template>
      <template slot="sjh" slot-scope="text">
        <div v-if="text == 'sjh'">手机号</div>

        <template slot="ra" slot-scope="text, row">
        {{ text }}
      </template>
      <template slot="pa" slot-scope="text, row">
        {{ text }}
      </template>

      </template>
      <!-- 删除 -->
      <template slot="operation" slot-scope="text, row">

        <a-button
          type="danger"
          @click=" ondel(row.id)"
          style="margin-right: 2rem"
          >删除</a-button
        >

        <a-button
          type="primary"
          @click="alterinfo(row.id)"
          style="margin-right: 2rem"
          >修改</a-button
        >
      </template>
    </a-table>


  </div>
</template>



<script >
import Footer from "@/components/Footer.vue";

// 表格表头
const columns = [
  {
    title: "ID",
    dataIndex: "id",
    key: 'id',
    width: "20%",
  },
  {
    title: "用户名称",
    dataIndex: "mc",
    key: 'mc',
    width: "20%",
    scopedSlots: { customRender: "mc" },
  },
  {
    title: "手机号",
    dataIndex: "sjh",
    key: 'sjh',
    width: "20%",
    scopedSlots: { customRender: "jys" },
  },
      {
    title: "用户资产",
    dataIndex: "ra",
    key: 'ra',
    width: "20%",
    scopedSlots: { customRender: "ra" },
  },
      {
    title: "盈亏资产",
    dataIndex: "pa",
    key: 'pa',
    width: "20%",
    scopedSlots: { customRender: "pa" },
  },


  {
    title: "操作",
    dataIndex: "operation",
    key: 'operation',
    scopedSlots: { customRender: "operation" },
  },
];


export default {
  name: "UserManage",
  props: {
    user_info: {
      type: Object,
    },
  },
  components: {
    Footer
  },
  data() {
    return {
      loading: false,
      searchLoading: false,
      data: [],
      columns,
      pagination: {
        pageSize: 5,
        current: 1,
      },
      dataSource: [], // 搜索框数据源
      userValue: "",
      userId: ""

    };
  },
  mounted() {
    let param = { 'pagenum': this.pagination.current, 'pagelimit': this.pagination.pageSize }
    this.getUsers(param)
  },

  methods: {
 /**
     * 处理表格分页
     */
    handleTableChange(pagination) {
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;

      this.getUsers({pagenum: this.pagination.current, pagelimit: this.pagination.pageSize});
      this.pagination.total = res.data.sum;


    },


    // ==================
    // 股票名称搜索框
    // ==================
    onSearchUser(searchText) {
      this.userValue = searchText;
    },
    /**
     * 点击搜索按钮
     */
    btnSearchUser() {
      // this.value_code = null
       if (this.userValue.trim().length==0){
          this.getUsers({pagenum: 1, pagelimit: this.pagination.pageSize});
        }

       else {
         this.getUserData(this.userValue);
       }
    },


    /**
     * 搜索框数据源获取
     */
    getUsers(param) {
      param = {
        pagelimit: param['pagelimit'],
        pagenum: param['pagenum']
      }
      this.$user_api.get_users(param).then((res) => {
        this.loading = true
        let dataSource = [];
        if (res.code == 200) {
          console.log(res);
          for (let i = 0; i < res.data.accounts.length; i++) {
            dataSource.push(
              {
                'mc': res.data.accounts[i]["nickname"],
                'id': res.data.accounts[i]['id'],
                'sjh': res.data.accounts[i]['phone'],
                'ra': this.formatAsset(res.data.accounts[i]['rest_asset']),
                'pa': this.formatAsset(res.data.accounts[i]['profit_asset'])
              }
            );
          }
          this.data = dataSource
          // 分页处理
          const pagination = { ...this.pagination };
          pagination.total = res.data.sum;
          this.pagination = pagination;
          this.loading = false
        }
      });
    },


    getUserData(param) {
      param={
        nickname:this.userValue
      }
        this.$user_api.get_userbyname(param).then((res) => {
          this.loading = true
          let dataSource = [];
          if (res.code == 200) {
            console.log(res);
            for (let i = 0; i < res.data.accounts.length; i++) {
              dataSource.push(
                  {
                    'mc': res.data.accounts[i]["nickname"],
                    'id': res.data.accounts[i]['id'],
                    'sjh': res.data.accounts[i]['phone'],
                    'ra': this.formatAsset(res.data.accounts[i]['rest_asset']),
                    'pa': this.formatAsset(res.data.accounts[i]['profit_asset'])
                  }
              );
            }
            this.data = dataSource
            // 分页处理
            const pagination = {...this.pagination};
            pagination.total = res.data.sum;
            this.pagination = pagination;
            this.loading = false
          }
         });
    },



// 用户删除
      deleteById(param) {
			var r=confirm("确认删除吗？");
			if (r==true){
      param={
        id:this.userId
        }
       this.$user_api.delete_user(param).then((res) => {
          if (res){
            // this.$message.success("")
            window.alert("已删除")
            window.location.reload()

          }

        });
      }
        else{
        window.alert("已取消")
			  }
			},

//传递id
 ondel(id) {
      this.userId = id;
      this.deleteById(this.userId)
    },
  //   //页面刷新
  // refresh() {
  //   this.$router.go(0)
  // },


//修改
    alterinfo(id){
      this.userId=id
      this.$router.push({
        path: `/user-update/`, query:{id:this.userId}
      });
    },

    //添加
    addUser(){
      this.$router.push({
        path: `/user-add/`,
      });
    },

    formatAsset(restAsset) {
          if (restAsset == undefined) {
              return 0.0000
          }
          return restAsset
      }


    },
};
</script>
