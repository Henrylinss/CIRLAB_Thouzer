# CIRLAB_Thouzer
- 分為三個裝置運行(小電腦、伺服器、筆記型電腦)
- 於小電腦和伺服器中使用ROS1系統
- 使用到的通訊系統
  > ROS

  > socket
  
  > mqtt 
  ## 小電腦(mini_PC)
- 負責與AGV溝通<font color='Red'>(mqtt)</font>和AMCL定位<font color='Red'>(ROS)</font>
  ## 伺服器(server_PC)
- 運行監控系統
- demo指令
  ## 筆記型電腦
- 傳輸<font color='Blue'>RGB影像</font>和<font color='Blue'>骨架資料</font><font color='Red'>(socket)</font>
