import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import './c3.css'
import Paper from '@material-ui/core/Paper';
import gear from './icons/file.svg'
import oil from './icons/iolDrop.svg'
import axios from 'axios'
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import LinearProgress from '@material-ui/core/LinearProgress';
import Divider from '@material-ui/core/Divider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import Chip from '@material-ui/core/Chip';
import ReactSpeedometer from "react-d3-speedometer"
import RTChart from 'react-rt-chart';

class App extends Component {
  constructor(props){
    super(props);
    this.state={
      status:"False",
      mean:[],
      m:0,
      std:0,
      peak:0,
      slope:0
    }
  }
  componentDidMount() {
    if(this.state.statu=="True"){
      this.handleStatus()
    }
  }

  

 
  handleStatus=()=>{
    this.setState({
      status:"True"
    })
      this.lookupInterval = setInterval(() => {
        axios
           .get('http://group-c.serveo.net/')
           .then(res=> {
             console.log(res.data.slope * 100000)
             this.setState({
               status:res.data.ok,
               m:res.data.mean,
               std:res.data.standardDeviation,
               peak:res.data.peakFrequency,
               slope:res.data.slope
              })
           })  
     }, 3000)
    

  }

  componentWillUnmount() {
    clearInterval(this.lookupInterval)
    this.stopCalling()
  }
  stopCalling=()=>{
    this.setState({
      status:"False"
    })
    clearInterval(this.lookupInterval)
  }


  render() {

    var data = {
      date: new Date(),
      Mean: this.state.m,
      StandartDev:this.state.std
    };
    var flow = {
      duration: 200
  };
var chart={
  axis: {
    y: { min:-3, max: 3 }
}
}
var percentage = (this.state.peak*100)/200
var slope = (this.state.slope*100000)
    const status=this.state.status;
    return (
      <div className="container">
      <AppBar position="static">
        <Toolbar variant="dense">
          <Typography variant="h4" color="inherit">
            Monitoring system
          </Typography>
        </Toolbar>
        </AppBar>

      <Grid container spacing={24}>
      
      <Grid item xs={12}>
          <Paper >
            <Grid container> 
              <Grid style={{textAlign:'center'}} item xs={2}>
              <img className="App-logo-gear" src={gear} alt=""/>
              </Grid>
              <Grid style={{textAlign:'center', marginTop:'10px'}} item xs={4}>
              <h4 className="display-4">STATUS</h4>
              </Grid>
              {status=="True"? <Grid style={{textAlign:'center'}} item xs={6} className="alert alert-success stopLight">
                          <h1>OK</h1>
                        </Grid>
              :<Grid style={{textAlign:'center'}} item xs={6} className="alert alert-danger">
                          <h1>Precaution</h1>
                        </Grid>}
              </Grid>
            
          </Paper>
        </Grid>

      
        
         {status=="False"? 
         <Grid item container>
         <Grid item onClick={this.stopCalling} xs={6}style={{marginTop:'10px'}} >
            <Button  variant="contained" color="primary" style={{backgroundColor:"Red"}} fullWidth	>
              STOP PROCESS
            </Button>     
         </Grid>
         <Grid item xs={6} onClick={this.handleStatus} style={{marginTop:'10px'}}>
            <Button   variant="contained"   style={{backgroundColor:"yellow"}} fullWidth	>
              IGNORE
            </Button>  
         </Grid>
         </Grid>
         :""}
          
        
         <Grid item xs={12} >
          <Paper>
          <RTChart
          chart={chart}
              flow={flow}
              fields={['Mean','StandartDev']}
              data={data} />
          </Paper>
         </Grid>

          <Grid item xs={6} >
            <Paper style={{padding:'10px',textAlign:'center'}}>

            <LinearProgress color="secondary" style={{width:'100%', height:'100px'}} variant="determinate" value={percentage} />
            <span style={{float:'left', textAlign:'left', marginTop:'5px'}}>
            <Chip
                label="low"
                color="secondary"
              />
              </span>
            <span style={{float:'right',textAlign:'right', marginTop:'5px'}} >
            <Chip
                label="high"
                color="secondary"
              />
            </span>
            <h4 style={{marginTop:'10px',marginBottom:'43px'}}>Frequency Peak</h4>

            </Paper>
          </Grid>
          <Grid item xs={6} >
            <Paper style={{padding:'10px'}}>

            <div style={{marginLeft:'57px'}}>
            <ReactSpeedometer 
                maxValue={4}
                minValue={-4}
                height={180}
                value={slope}
                needleColor="black"
                startColor="#ffbd66"
                segments={10}
                endColor="#ff9100"
                textColor="grey"
              />
            </div>
            </Paper>
          </Grid>


      </Grid>

      </div>
    );
  }
}

export default App;
