<template>
  <div>
    <a-row type="flex">
    <a-col flex="40%" style="margin-left:5rem;">
        <!-- 搜索自选股对话框 -->
        <div>
          <span>股票名称：</span>
          <a-auto-complete
            v-model="input"
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
        <a-button type="primary" @click="add_s">
         添加数据
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
      <!-- 购入详情页面 -->
      <template slot="index" slot-scope="text">
        {{ text }}
      </template>
      <template slot="dm" slot-scope="text, row">
        {{ text }}
      </template>
      <template slot="mc" slot-scope="text, row">
        {{ text }}
      </template>
      <template slot="num" slot-scope="text">
        {{ text }}
      </template>
      <template slot="bp" slot-scope="text">
       {{ text }}
      </template>
      <template slot="bt" slot-scope="text">
       {{ text }}
      </template>
       <template slot="p" slot-scope="text">
       {{ text }}
      </template>
      <template slot="uid" slot-scope="text">
        {{ text }}
      </template>

      <!-- 删除 -->
      <template slot="operation" slot-scope="text, row">

        <a-button
          type="danger"
          @click="del_s(row.index)"
          style="margin-right: 2rem"
          >删除</a-button
        >

        <a-button
          type="primary"
          @click="up_s(row.index)"
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
    title: "Index",
    dataIndex: "index",
    key: 'index',
    width: "10%",
  },
    {
    title: "股票代码",
    dataIndex: "dm",
    key: 'dm',
    width: "10%",
    scopedSlots: { customRender: "dm" },
  },

  {
    title: "股票名称",
    dataIndex: "mc",
    key: 'mc',
    width: "13%",
    scopedSlots: { customRender: "mc" },
  },
  {
    title: "买入数量(单位：股)",
    dataIndex: "num",
    key: 'num',
    width: "10%",
    scopedSlots: { customRender: "num" },
  },
  {
    title: "买入价格(单位：股)",
    dataIndex: "bp",
    key: 'bp',
    width: "10%",
    scopedSlots: { customRender: "bp" },
  },

  {
    title: "买入时间",
    dataIndex: "bt",
    key: 'bt',
    width: "15%",
    scopedSlots: { customRender: "bt" },
  },
  {
    title: "收益",
    dataIndex: "p",
    key: 'p',
    width: "10%",
    scopedSlots: { customRender: "p" },
  },

  {
    title: "所属用户ID",
    dataIndex: "uid",
    key: 'uid',
    width: "10%",
    scopedSlots: { customRender: "uid" },
  },

      {
    title: "操作",
    dataIndex: "operation",
    key: 'operation',
    width: "10%",
    scopedSlots: { customRender: "operation" },
  },


];


export default {
  name: "UserMoney",
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
      input: "",


    };
  },
  mounted() {
    this.stock_all()
  },

  methods: {
 /**
     * 处理表格分页
     */
    handleTableChange(pagination) {
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.stock_all()
    },


    // ==================
    // 股票名称搜索框
    // ==================
    onSearchUser(searchText) {
      this.input = searchText;
    },
    /**
     * 点击搜索按钮
     */
    btnSearchUser() {
      // this.value_code = null
       if (this.input.trim().length==0){
          this.stock_all();
        }

       else {
         this.stock_one();
       }
    },


    /**
     * 搜索框数据源获取
     */
    stock_all() {
      this.$alipay_api.q_all().then((res) => {
        this.loading = true
        let dataSource = [];
        if (res.code == 200) {
          console.log(res);
             for (let i = 0; i < res.data.stocks.length; i++) {
              dataSource.push(
                  {
                    'index': res.data.stocks[i]["index"],
                    'dm': res.data.stocks[i]["code_id"],
                    'mc': res.data.stocks[i]['stockname'],
                    'num': res.data.stocks[i]['stocknum'],
                    'bt': res.data.stocks[i]['buy_time'],
                    'bp': res.data.stocks[i]['buy_price'],
                    'p':this.formatProfit( res.data.stocks[i]['pofit']),
                    'uid': res.data.stocks[i]['account_id'],
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




      stock_one(){
      let param={
        search:this.input,
      }
        this.$alipay_api.q_one(param).then((res) => {
          this.loading = true
          let dataSource = [];
          if (res.code == 200) {
            console.log(res);
            for (let i = 0; i < res.data.stocks.length; i++) {
              dataSource.push(
                {
                    'index': res.data.stocks[i]["index"],
                    'dm': res.data.stocks[i]["code_id"],
                    'mc': res.data.stocks[i]['stockname'],
                    'num': res.data.stocks[i]['stocknum'],
                    'bp': res.data.stocks[i]['buy_price'],
                    'bt': res.data.stocks[i]['buy_time'],
                    'p':this.formatProfit( res.data.stocks[i]['pofit']),
                    'uid': res.data.stocks[i]['account_id']
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


    add_s(){
      this.$alipay_api.add_stock().then((res) => {
          if (res.code==200){
            this.$message.success("添加成功")
          }
      })
    },


    del_s(index){
      this.$alipay_api.del_stock(index).then((res) => {
          if (res.code==200){
            this.$message.success("删除成功")
          }
      })
    },

    up_s(index){
      this.$alipay_api.update_stock(index).then((res) => {
            if (res.code==200){
            this.$message.success("修改成功")
          }
      })
    },


  //   //页面刷新
  // refresh() {
  //   this.$router.go(0)
  // },
  formatProfit(profit) {
          if (profit == undefined) {
              return 0.0000
          }
          return profit
      }






    },
};
</script>
