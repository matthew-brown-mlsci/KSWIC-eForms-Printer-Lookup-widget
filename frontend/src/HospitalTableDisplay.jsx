import React from 'react';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

//import "react-tabulator/lib/styles.css"; // default theme
//import "./tabulator_bootstrap.min.css"; // use Theme(s)
import { ReactTabulator, reactFormatter } from "react-tabulator"; // for React 15.x

import 'react-app-polyfill/ie11'

import './config';


const useStyles = makeStyles((theme) => ({
    root: {
      // backgroundColor: theme.palette.background.paper,
      'display': "contents",
      '& .MuiTextField-root': {
        margin: theme.spacing(1),
        width: '50ch',
      },
    },
    '& > *': {
      margin: theme.spacing(1),
    },
    paper: {
      position: 'absolute',
      width: 400,
      backgroundColor: theme.palette.background.paper,
      border: '2px solid #000',
      boxShadow: theme.shadows[5],
      padding: theme.spacing(2, 4, 3),
    },
    save: {
      backgroundColor: '#13AB0C ',
      color: 'white',
    },
    cancel: {
      backgroundColor: '#FFC300',
      color: 'white',
    },
    delete: {
      backgroundColor: '#C70039',
      color: 'white',
    }
  
  }));


class HospitalTableDisplay extends React.Component {
    constructor(props) {
      super(props);
    }
   
    render() {
      //console.info('HospitalTableDisplay: this.props');
      //console.info(this.props);
      return (
        <div>{this.props.isLoggedIn ? <HospitalTabulator isLoggedIn={this.props.isLoggedIn} access_level={this.props.access_level} pchost={this.props.pchost} 
                                                                       userID={this.props.userID} domain={this.props.domain} 
                                                                       hospTable={this.props.hospTable} setHospTable={this.props.setHospTable}
                                                                       origRows={this.props.origRows} setOrigRows={this.props.setOrigRows} 
                                                                       session_passkey={this.props.session_passkey} set_session_passkey={this.props.set_session_passkey}/> : ErrorGreeting()} </div>
      );
    }
  }
  
  
  
  function ErrorGreeting() {
    return (<div>
              <h3>Error, this website requires user provisioning.</h3>
              <br />
              <h2>
              </h2>
              <br />
              <p>If you require access to this site, please contact the Clinical Admin group: ais-dl-eca-clinicaladmin@ascension.org</p>
            </div>
          );
  }
  
  function SaveButtonPrettySmall(props) {
    const classes = useStyles();
    var disable_button = false;
  
    if (props.cell._cell.row.data.colorcode == 'saving') {
      disable_button = true;
    } 
    if (props.cell._cell.row.data.colorcode == 'saved') {
      disable_button = true;
    } 
    if (props.cell._cell.row.data.colorcode == 'deleted') {
      disable_button = true;
    }
    if (props.cell._cell.row.data.colorcode == 'deleting') {
      disable_button = true;
    } 
    return (
      <Button variant="contained" className={classes.save} size="small" disabled={disable_button}>{props.cell._cell.element.title}</Button>
    );
  }
  
  function CancelButtonPrettySmall(props) {
    const classes = useStyles();
    var disable_button = false;
  
    if (props.cell._cell.row.data.colorcode == 'saving') {
      disable_button = true;
    } 
    if (props.cell._cell.row.data.colorcode == 'saved') {
      disable_button = true;
    } 
    if (props.cell._cell.row.data.colorcode == 'deleted') {
      disable_button = true;
    }
    if (props.cell._cell.row.data.colorcode == 'deleting') {
      disable_button = true;
    } 
    //console.info("CancelButtonPrettySmall");
    //console.info(props);
    return (
      <Button variant="contained" className={classes.cancel} size="small" disabled={disable_button}>{props.cell._cell.element.title}</Button>
    );
  }
  
  function DeleteButtonPrettySmall(props) {
    const classes = useStyles();
    var disable_button = false;
  
    if (props.cell._cell.row.data.colorcode == 'deleting') {
      disable_button = true;
    } 
    if (props.cell._cell.row.data.colorcode == 'deleted') {
      disable_button = true;
    }
  
    return (
      <Button variant="contained" className={classes.delete} size="small" disabled={disable_button}>{props.cell._cell.element.title}</Button>
    );
  }
  
  
  class HospitalTabulator extends React.Component {
    constructor(props) {
      super(props);
      var self = this;
      //console.info(this);
      this.state = {
        columns: [
          { title: "PC ID", field: "pc_id", width: 180, editor: 'input', hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "Printer", field: "printer", width: 180, editor: 'input', hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "Notes", field: "notes", editor: 'input', hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "Created", field: "created", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "Created By", field: "createdby", width: 130, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "Edited", field: "edited", width: 150, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "Edited By", field: "editedby", width: 130, hozAlign: "left", headerFilter:"input", headerFilterPlaceholder:" " },
          { title: "", field:"save", hozAlign:"left", formatter:reactFormatter(<SaveButtonPrettySmall />), width:80, headerSort:false},
          { title: "", field:"cancel", hozAlign:"left", formatter:reactFormatter(<CancelButtonPrettySmall />), width:80, headerSort:false},
          { title: "", field:"delete", hozAlign:"left", formatter:reactFormatter(<DeleteButtonPrettySmall />), width:80, headerSort:false}
        ],
        original_rows: {},
        options: {
          height: (window.innerHeight - 405).toString() + "px",
          movableRows: false,
          tooltips:true,
          selectable:false,
          dataLoaded:function(data){
            //console.info("dataLoaded");
            //console.info(data);
            //console.info(this);
            self.props.setHospTable(this);
            self.props.setOrigRows(JSON.parse(JSON.stringify(self.state.original_rows)));
            //console.info(self.state.original_rows);
            //console.info(self.props);
          },
          rowAdded:function(row){
            //console.info("rowAdded");
            //console.info(row);
            //console.info(self.props.origRows);
  
            self.state.original_rows = JSON.parse(JSON.stringify(self.props.origRows));
          },
          cellEdited:function(cell){
            //console.info("cellEdited: ");
            //console.info(cell);
            //console.info(this);
            //console.info(self);
            var updated_data = JSON.parse(JSON.stringify(cell._cell.row.data));
            updated_data.colorcode = 'edited';
            //console.info(updated_data);
            this.updateData([updated_data]);
          },
          rowFormatter:function(row){
              var data = row.getData();
              if (data.colorcode == "edited"){
                //console.info(row);
                row.getElement().style.backgroundColor = "#F6FD80"; //apply css change to row element
              } else if (data.colorcode == "not edited") {
                row.getElement().style.backgroundColor = "#FFFFFF";
              } else if (data.colorcode == "saved") {
                row.getElement().style.backgroundColor = "#2AE833"; //apply css change to row element
              } else if (data.colorcode == "failed to save") {
                row.getElement().style.backgroundColor = "#F06767"; //apply css change to row element
              } else if (data.colorcode == "deleting") {
                row.getElement().style.backgroundColor = "#e65ad8"; //apply css change to row element
              } else if (data.colorcode == "deleted") {
                row.getElement().style.backgroundColor = "#de4765"; //apply css change to row element
              }
          },
          //setData:function() {this.setState({ data });},
          //ajaxProgressiveLoad: 'scroll',
          //ajaxFiltering: true,
          //ajaxProgressiveLoadDelay: 200,
          //ajaxProgressiveLoadScrollMargin: 100,
          ajaxURL: global.config.conf.api_endpoint + 'selectAllHospitalRows',
          cellClick:function(e, cell){ //trigger an alert message when the row is clicked
            //console.info(e);
            //console.info(cell);
            if (cell._cell.column.field === 'delete') {
              //console.info('delete clicked!');
              var thisTabulator = this;
              var delete_row_id = cell._cell.row.data.id;
              var delete_row_hospital_key = cell._cell.row.data.hospital_key;
              var save_row_editedby = self.props.domain + '\\' + self.props.userID;
  
              var delete_row_in_process = JSON.parse(JSON.stringify(cell._cell.row.data));
              delete_row_in_process['colorcode'] = 'deleting';
              delete_row_in_process['delete'] = "Deleting...";
              thisTabulator.updateData([delete_row_in_process]);
  
              // Select the row first, store the values for the changelog entry that will be added
              var target_url = global.config.conf.api_endpoint + 'selectOneHospitalRow';
              var url_args = {hospital_key: delete_row_hospital_key,
                              samAccountName: self.props.userID,
                              domain: self.props.domain,
                              passkey: self.props.session_passkey
                             }
              var original_row_to_delete = [];
              $.ajax({
                url: target_url,
                data: url_args,
                type: "GET",  
                dataType: "jsonp",
                timeout: 15000,
                success: function(data) {
                  if (data.success === true) {
                    //console.info(target_url + '  :  ' + 'success == true');
                    //console.info(cell._cell.row);
                    //console.info(data);
                    //console.info(self);
                    for (var row in data.data) {
                      if (data.data[row].id == cell._cell.row.data.id) {
                        original_row_to_delete = JSON.parse(JSON.stringify(data.data[row]));
                        //console.info('original_row_to_delete');
                        //console.info(original_row_to_delete);
                      }
                    }
                  }
                  else {
                    //console.info(target_url + '  :  ' + 'success == false');
                    //console.info(data);
                    //console.info(self);
                  }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                  //console.info(target_url + '  :  ' + 'ajax request failed');
                }
              }).then(function(promise_data){
                var target_url = global.config.conf.api_endpoint + 'deleteOneHospitalRow';
                var url_args = {hospital_key: delete_row_hospital_key,
                                samAccountName: self.props.userID,
                                domain: self.props.domain,
                                passkey: self.props.session_passkey
                              }
                $.ajax({
                  url: target_url,
                  data: url_args,
                  type: "GET",  
                  dataType: "jsonp",
                  timeout: 15000,
                  success: function(data) {
                    if (data.success === true) {
                      //console.info(target_url + '  :  ' + 'success == true');
                      delete_row_in_process['colorcode'] = 'deleted';
                      delete_row_in_process['delete'] = "Removed";
                      thisTabulator.updateData([delete_row_in_process]);
                      setTimeout(function() {
                        var copy_original_rows = JSON.parse(JSON.stringify(self.state.original_rows));
                        for (var copy_original_row in copy_original_rows) {
                          if (copy_original_rows[copy_original_row].id === delete_row_in_process.id) {
                            self.state.original_rows.splice(copy_original_row, 1);
                            thisTabulator.deleteRow(delete_row_in_process.id);
                          }
                        }
                      }, 10000);
                      //console.info(data);
                      //console.info(self);
                    }
                    else {
                      //console.info(target_url + '  :  ' + 'success == false');
                      //console.info(data);
                      //console.info(self);
                      var delete_error_row = JSON.parse(JSON.stringify(cell._cell.row.data));
                      delete_row_in_process['delete'] = "API Error";
                      delete_row_in_process['colorcode'] = 'failed to save';
                      thisTabulator.updateData([delete_row_in_process]);
                      setTimeout(function() {
                        for (var original_row in self.state.original_rows) {
                          if (self.state.original_rows[original_row].id === delete_row_in_process.id) {
                            thisTabulator.updateData([JSON.parse(JSON.stringify(self.state.original_rows[original_row]))]);
                          }
                        }
                      }, 10000);
                    }
                  },
                  error: function(jqXHR, textStatus, errorThrown) {
                    //console.info(target_url + '  :  ' + 'ajax request failed');
                    var delete_error_row = JSON.parse(JSON.stringify(cell._cell.row.data));
                    delete_row_in_process['delete'] = "API Error";
                    delete_row_in_process['colorcode'] = 'failed to save';
                    thisTabulator.updateData([delete_row_in_process]);
                    setTimeout(function() {
                      for (var original_row in self.state.original_rows) {
                        if (self.state.original_rows[original_row].id === delete_row_in_process.id) {
                          thisTabulator.updateData([JSON.parse(JSON.stringify(self.state.original_rows[original_row]))]);
                        }
                      }
                    }, 10000);
                  }
                }).then(function(promise_data){
                  var log_entry = 'Delete record';
                  var notes = JSON.stringify({previous_row: {
                                                              pc_id: original_row_to_delete.pc_id,
                                                              printer: original_row_to_delete.printer,
                                                              notes: original_row_to_delete.notes,
                                                              editedby: original_row_to_delete.editedby
                                                            }
                                             });
                  var old_pc_id = original_row_to_delete.pc_id
                  var old_printer = original_row_to_delete.printer;
                  var createdby = self.props.userID;
                  var domain = self.props.domain;
                  var createdby_host = self.props.pchost;
                  var environment = 'prod';
  
                  var target_url = global.config.conf.api_endpoint + 'addOneChangelogRow';
                  var url_args = { log_entry: log_entry,
                                   old_pc_id: old_pc_id,
                                   old_printer: old_printer,
                                   environment: environment,
                                   notes: notes,
                                   createdby: createdby,
                                   createdby_host: createdby_host,
                                   samAccountName: self.props.userID,
                                   domain: self.props.domain,
                                   passkey: self.props.session_passkey
                                 }
                  //console.info(url_args);
                  $.ajax({
                    url: target_url,
                    data: url_args,
                    type: "GET",  
                    dataType: "jsonp",
                    timeout: 15000,
                    success: function(data) {
                      if (data.success === true) {
                        //console.info(target_url + '  :  ' + 'success == true');
                        //console.info(data);
                      }
                      else {
                        //console.info(target_url + '  :  ' + 'success == false');
                        //console.info(data);
                      }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                      //console.info(target_url + '  :  ' + 'ajax request failed');
                      //console.info(textStatus);
                      //console.info(errorThrown);
                    }
                  });
  
                });
              });
            }
            if (cell._cell.column.field === 'save') {
              //document.body.classList.add('busy-cursor');
              //console.info(cell._cell.row.data);
              //console.info(this);
              var thisTabulator = this;
              //console.info(self);
  
              // Indicated we're processing the request
              var save_row_in_process = JSON.parse(JSON.stringify(cell._cell.row.data));
              save_row_in_process['colorcode'] = 'saving';
              save_row_in_process['save'] = "Saving";
              thisTabulator.updateData([save_row_in_process]);
  
              
  
  
              //thisTabulator.redraw();
              // Collect new values to use in ajax call
              var save_row_id = cell._cell.row.data.id;
              var save_row_hospital_key = cell._cell.row.data.hospital_key;
              var save_row_pc_id = cell._cell.row.data.pc_id;
              var save_row_printer = cell._cell.row.data.printer;
              var save_row_notes = cell._cell.row.data.notes;
              var save_row_editedby = self.props.domain + '\\' + self.props.userID;
              var previous_row = {};
              var new_row = {};
              
              // Select the current row before updating, that way we have the current row object to put in the changelog
              var target_url = global.config.conf.api_endpoint + 'selectOneHospitalRow';
              var url_args = {hospital_key: save_row_hospital_key,
                              samAccountName: self.props.userID,
                              domain: self.props.domain,
                              passkey: self.props.session_passkey
                            }
              $.ajax({
                url: target_url,
                data: url_args,
                type: "GET",  
                dataType: "jsonp",
                timeout: 15000,
                success: function(data) {
                  if (data.success === true) {
                    //console.info(target_url + '  :  ' + 'success == true');
                    //console.info(cell._cell.row);
                    //console.info(data);
                    //console.info(self);
                    for (var row in data.data) {
                      if (data.data[row].id == cell._cell.row.data.id) {
                        previous_row = JSON.parse(JSON.stringify(data.data[row]));
                      }
                    }
                  }
                  else {
                    //console.info(target_url + '  :  ' + 'success == false');
                    //console.info(data);
                    //console.info(self);
                  }
                },
                error: function(jqXHR, textStatus, errorThrown) {
                  //console.info(target_url + '  :  ' + 'ajax request failed');
                }
              }).then(function(promise_data){
                var target_url = global.config.conf.api_endpoint + 'addOrUpdateOneHospitalRow';
                var url_args = {id: save_row_id,
                                hospital_key: save_row_hospital_key,
                                pc_id: save_row_pc_id,
                                printer: save_row_printer,
                                notes: save_row_notes,
                                editedby: save_row_editedby,
                                samAccountName: self.props.userID,
                                domain: self.props.domain,
                                passkey: self.props.session_passkey
                              }
                self.state.addOrUpdateOneHospitalRow_url_args = JSON.parse(JSON.stringify(url_args));
  
  
                $.ajax({
                  url: target_url,
                  data: url_args,
                  type: "GET",  
                  dataType: "jsonp",
                  timeout: 15000,
                  success: function(data) {
                    if (data.success === true) {
                      //console.info(target_url + '  :  ' + 'success == true');
                      self.state.addOrUpdateOneHospitalRow_data = data;
                      //console.info(data);
                      //console.info(self);
                    }
                    else {
                      //console.info(target_url + '  :  ' + 'success == false');
                      //console.info(data);
                      //console.info(self);
                      var save_error_row = JSON.parse(JSON.stringify(cell._cell.row.data));
                      save_error_row['save'] = "API Error";
                      save_error_row['colorcode'] = 'failed to save';
                      thisTabulator.updateData([save_error_row]);
                      setTimeout(function() {
                        for (var original_row in self.state.original_rows) {
                          if (self.state.original_rows[original_row].id === save_error_row.id) {
                            thisTabulator.updateData([JSON.parse(JSON.stringify(self.state.original_rows[original_row]))]);
                          }
                        }
                      }, 5000);
                    }
                  },
                  error: function(jqXHR, textStatus, errorThrown) {
                    //console.info(target_url + '  :  ' + 'ajax request failed');
                    var save_error_row = JSON.parse(JSON.stringify(cell._cell.row.data));
                      save_error_row['save'] = "API Error";
                      save_error_row['colorcode'] = 'failed to save';
                      thisTabulator.updateData([save_error_row]);
                      setTimeout(function() {
                        for (var original_row in self.state.original_rows) {
                          if (self.state.original_rows[original_row].id === save_error_row.id) {
                            thisTabulator.updateData([JSON.parse(JSON.stringify(self.state.original_rows[original_row]))]);
                          }
                        }
                      }, 5000);
                  }
                }).then(function(promise_data){
                  //console.info('made it to then() clause for selectOneHospitalRow');
                  //console.info(promise_data);
                  var target_url = global.config.conf.api_endpoint + 'selectOneHospitalRow';
                  var url_args = {hospital_key: save_row_hospital_key,
                                  samAccountName: self.props.userID,
                                  domain: self.props.domain,
                                  passkey: self.props.session_passkey
                                }
                  $.ajax({
                    url: target_url,
                    data: url_args,
                    type: "GET",  
                    dataType: "jsonp",
                    timeout: 15000,
                    success: function(data) {
                      if (data.success === true) {
                        //console.info(target_url + '  :  ' + 'success == true');
                        //console.info(cell._cell.row);
                        //console.info(data);
                        //console.info(self);
                        for (var row in data.data) {
                          if (data.data[row].id == cell._cell.row.data.id) {
                            new_row = JSON.parse(JSON.stringify(data.data[row]));
                            data.data[row]['save'] = "Saved!";
                            data.data[row]['cancel'] = "Cancel";
                            data.data[row]['delete'] = "Delete";
                            data.data[row]['colorcode'] = 'saved';
                            //console.info('updating a row with: ' + target_url);
                            //console.info(data.data[row]);
                            thisTabulator.updateData([JSON.parse(JSON.stringify(data.data[row]))]);
                            setTimeout(function() {
                              data.data[row]['save'] = "Save";
                              data.data[row]['colorcode'] = "not edited";
                              thisTabulator.updateData([JSON.parse(JSON.stringify(data.data[row]))]);
                            }, 5000);
                          }
                        }
                      }
                      else {
                        //console.info(target_url + '  :  ' + 'success == false');
                        //console.info(data);
                        //console.info(self);
                      }
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                      //console.info(target_url + '  :  ' + 'ajax request failed');
                    }
                  }).then(function(promise_data, test_var){
                    //console.info(promise_data);
                    // add a row to changelog
                    //console.info('changelog ajax call()');
                    //console.info(promise_data);
                    //console.info(test_var);
                    //console.info(self.state.addOrUpdateOneHospitalRow_data);
                    //console.info(self.state.addOrUpdateOneHospitalRow_url_args);
                    //console.info(self.state.original_rows);
  
                    //for (var row in self.state.original_rows) {
                    //  if (self.state.original_rows[row].id === self.state.addOrUpdateOneHospitalRow_url_args.id) {
                    //    var old_pc_id = self.state.original_rows[row].pc_id;
                    //    var old_printer = self.state.original_rows[row].printer;
                    //  }
                    //}
  
                    //console.info(old_pc_id);
                    //console.info(old_printer);
                    //console.info(self.props);
  
                    var log_entry = 'Update record';
                    var notes = JSON.stringify({previous_row: {
                                                                pc_id: previous_row.pc_id,
                                                                printer: previous_row.printer,
                                                                notes: previous_row.notes,
                                                                editedby: previous_row.editedby
                                                              },
                                                new_row:      {
                                                                pc_id: new_row.pc_id,
                                                                printer: new_row.printer,
                                                                notes: new_row.notes,
                                                              }
                                               });
                    //var new_pc_id = self.state.addOrUpdateOneHospitalRow_url_args.pc_id;
                    //var new_printer = self.state.addOrUpdateOneHospitalRow_url_args.printer;
                    var createdby = self.props.userID;
                    var domain = self.props.domain;
                    var createdby_host = self.props.pchost;
                    var environment = 'prod';
  
                    var target_url = global.config.conf.api_endpoint + 'addOneChangelogRow';
                    var url_args = { log_entry: log_entry,
                                    old_pc_id: previous_row.pc_id,
                                    new_pc_id: new_row.pc_id,
                                    old_printer: previous_row.printer,
                                    new_printer: new_row.printer,
                                    environment: environment,
                                    notes: notes,
                                    createdby: createdby,
                                    createdby_host: createdby_host,
                                    samAccountName: self.props.userID,
                                    domain: self.props.domain,
                                    passkey: self.props.session_passkey
                                  }
                    
                    $.ajax({
                      url: target_url,
                      data: url_args,
                      type: "GET",  
                      dataType: "jsonp",
                      timeout: 15000,
                      success: function(data) {
                        if (data.success === true) {
                          //console.info(target_url + '  :  ' + 'success == true');
                          //console.info(data);
                        }
                        else {
                          //console.info(target_url + '  :  ' + 'success == false');
                          //console.info(data);
                        }
                      },
                      error: function(jqXHR, textStatus, errorThrown) {
                        //console.info(target_url + '  :  ' + 'ajax request failed');
                        //console.info(textStatus);
                        //console.info(errorThrown);
                      }
                    });
                  });
                });
              });
              //console.info(self.state.original_rows);
              //rebootserver(cell._cell.row.data);
            }
            if (cell._cell.column.field === 'cancel') {
                //console.info(cell._cell.row.data);
                //console.info(this);
                //console.info(self.state);
                var cancel_row_id = cell._cell.row.data.id;
                for (var original_row in self.state.original_rows) {
                  if (self.state.original_rows[original_row].id === cancel_row_id) {
                    //console.info('original data:');
                    //console.info(self.state.original_rows[original_row]);
                    this.updateData(JSON.parse(JSON.stringify([self.state.original_rows[original_row]])));
                    cell._cell.row.getElement().style.backgroundColor = "#FFFFFF";
                  }
                }
              }
            },
          ajaxRequestFunc: function(url, config, params) {
            //console.log('Made it to ajaxRequestFunc');
            //console.log('url, config, params');
            //console.info(url);
            //console.info(config);
            params = {samAccountName: self.props.userID,
                      domain: self.props.domain,
                      passkey: self.props.session_passkey}
            //console.info(params);
  
            return new Promise(function(resolve, reject){
              $.ajax({
                url: url,
                data: params,
                type: "GET",  
                dataType: "jsonp",
                timeout: 15000,
                success: function(data) {
                  if (data.success === true) {
                    for (var row in data.data) {
                      //data.data[row]['save'] = "<input id=\"input_id_save_" + data.data[row].id + "\" type=\"button\" value=\"Save\"/>";
                      data.data[row]['save'] = "Save";
                      data.data[row]['cancel'] = "Cancel";
                      data.data[row]['delete'] = "Delete";
                      data.data[row]['colorcode'] = 'not edited';
                    }
                    self.state.original_rows = JSON.parse(JSON.stringify(data.data));
                    //console.info("end success orig ajax call");
                    //self.props.setHospTable(self);
                    //console.info(self.props);
                    //console.info(data);
                    //self.props.tabletalk = self;
                    //console.info(self);
                    //console.info(this);
                    resolve(data.data);
                  }
                  else {
                    reject();
                  }
                  },
                error: function(jqXHR, textStatus, errorThrown) {
                  reject();
                }
              });
            });
          },
          current_page: 1,
          paginationSize: 50,
          ajaxResponse: function(url, params, response) {
            //console.log('ajaxResponse', url);
            return response; //return the response data to tabulator
          },
          ajaxError: function(error) {
            //console.log('ajaxError', error);
          }
        }
      };
  
    }
  
    render() {
      return (
        <div>
          <ReactTabulator
                ref={ref => (this.ref = ref)}
                columns={this.state.columns}
                data={[]}
                //height={(window.innerHeight - 370).toString() + "px"}
                //rowClick={this.rowClick}
                options={this.state.options}
                data-custom-attr="test-custom-attribute"
                className="custom-css-class"
              />
        </div>
      );
    }
  }
  
export default HospitalTableDisplay;