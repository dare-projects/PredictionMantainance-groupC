<Paper style={{marginTop:'10px'}}>
        <div className="row">
          
            <div className="col-1">
              <img className="App-logo-gear" src={gear} alt=""/>
              <img src={oil} className="App-logo-iol" alt=""/>
            </div>
            <div className="col-3">
              <h4 className="display-4">STATUS</h4>
            </div>
            <div className="col-7">
              <div style={{marginTop:'10px'}} className="container">
                <div className="row stoplight">
                  <div  className="col-8 alert alert-success stopLight">OK</div>
                  {isFalse ? 
                            <div className="col-4">
                            <button className="btn btn-warning btn-block">Ignore</button>
                            <button className="btn btn-danger btn-block">Stop</button>
                            </div>
                            : <div className="col-4"></div>}
                </div>
              </div>
            </div>
          
          
        </div>
        </Paper>

        <Paper style={{marginTop:'10px'}}>
        <div className="row">
    <div className="col">Graph1 </div>
    <div className="col">Plot 2</div>
    <div className="w-100"></div>
    <div className="col">Plot 3</div>
    <div className="col">Plot 4</div>
  </div>
        </Paper>
