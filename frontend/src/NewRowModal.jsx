import React from 'react';

import { makeStyles, useTheme } from '@material-ui/core/styles';
import Modal from '@material-ui/core/Modal';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

import 'react-app-polyfill/ie11';
//import 'react-app-polyfill/stable'

//import { polyfill } from 'es6-promise'; polyfill();
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

function getModalStyle() {
    const top = 50;
    const left = 50;

    return {
        top: `${top}%`,
        left: `${left}%`,
        transform: `translate(-${top}%, -${left}%)`,
    };
}


function NewRowModal(props) {
    //console.info('NewRowModal()');
    //console.info(props);
  
    const classes = useStyles();
    // getModalStyle is not a pure function, we roll the style only on the first render
    const [modalStyle] = React.useState(getModalStyle);
    const [open, setOpen] = React.useState(false);
    const [pc_id_input_line, set_pc_id_input_line] = React.useState(false);
    const [printer_input_line, set_printer_input_line] = React.useState(false);
    const [notes_input_line, set_notes_input_line] = React.useState(false);
    const [error_notification, set_error_notification] = React.useState("");
    const [save_button_disabled, set_save_button_disabled] = React.useState(false);
    const [save_button_text, set_save_button_text] = React.useState('Save');
  
    const handleOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };
  
    const body = (
      <div style={modalStyle} className={classes.paper}>
        <h2 id="simple-modal-title">Add new row:</h2>
        <FormPropsTextFields pc_id_input_line={pc_id_input_line} set_pc_id_input_line={set_pc_id_input_line} 
                             printer_input_line={printer_input_line} set_printer_input_line={set_printer_input_line}
                             notes_input_line={notes_input_line} set_notes_input_line={set_notes_input_line} />
        <center>
          <br />
          <Button variant="contained" 
                  className={classes.save}
                  disabled={save_button_disabled}
                  onClick={() => { addHospTableRow(props, handleClose, set_error_notification, pc_id_input_line, printer_input_line, notes_input_line, set_save_button_disabled, set_save_button_text); }}>
            {save_button_text}</Button>
          {'    '}
          <Button variant="contained" className={classes.cancel} type="button" onClick={handleClose}>Cancel</Button>
          <br />{' '}<br />
          <h3 style={{color: "red"}}>{error_notification}</h3>
        </center><br />
      </div>
    );
  
    return (
      <div>
        <center><Button variant="contained" className={classes.save} onClick={handleOpen}>
            New row
          </Button></center><br />
        <Modal
          open={open}
          onClose={handleClose}
          aria-labelledby="simple-modal-title"
          aria-describedby="simple-modal-description"
        >
          {body}
        </Modal>
      </div>
    );
  }

  
function addHospTableRow(props, handleClose, set_error_notification, pc_id_input_line, printer_input_line, notes_input_line, set_save_button_disabled, set_save_button_text) {
    if (props.hospTable) {
      //console.info("addHospTableRow props");
      //console.info(props);
      //console.info(pc_id_input_line.value);
      //console.info(printer_input_line.value);
      //console.info(notes_input_line.value);
  
      set_save_button_disabled(true);
      set_save_button_text('Saving...');
  
      var insert_data_response = {};
  
      var target_url = global.config.conf.api_endpoint + 'addOrUpdateOneHospitalRow';
      var url_args = {pc_id: pc_id_input_line.value,
                      printer: printer_input_line.value,
                      notes: notes_input_line.value,
                      createdby: (props.domain + '\\' + props.userID),
                      samAccountName: props.userID,
                      domain: props.domain,
                      passkey: props.session_passkey
            };
      var new_row_from_api = {};
  
      //console.info(url_args);
      
      $.ajax({
        url: target_url,
        data: url_args,
        type: "GET",  
        dataType: "jsonp",
        timeout: 15000,
        success: function(data) {
          if (data.success === true) {
            //console.info(target_url + '  :  add new row : ' + 'success == true');
            //console.info(data);
            //console.info(self);
            insert_data_response = JSON.parse(JSON.stringify(data));
          }
          else {
            //console.info(target_url + '  : add new row :  ' + 'success == false');
            //console.info(data);
            //console.info(self);
            set_error_notification("Error - ajax request to API endpoint failed : " + target_url);
            set_save_button_disabled(true);
            set_save_button_text('Error');
            setTimeout(function() {
              set_error_notification("");
              set_save_button_disabled(false);
              set_save_button_text('Save');
            }, 10000);
          }
        },
        error: function(jqXHR, textStatus, errorThrown) {
          //console.info(target_url + '  :  ' + 'ajax request failed');
          //console.info(self);
          //console.info(this);
          //console.info(props);
          set_error_notification("Error - ajax request to API endpoint failed : " + target_url);
          set_save_button_disabled(true);
          set_save_button_text('Error');
          setTimeout(function() {
            set_error_notification("");
            set_save_button_disabled(false);
            set_save_button_text('Save');
          }, 10000);
        }
      }).then(function(promise_data){
          //console.info('made it to then() clause for selectOneHospitalRow');
          //console.info(promise_data);
          var target_url = global.config.conf.api_endpoint + 'selectOneHospitalRow';
          var url_args = {pc_id: pc_id_input_line.value,
                          samAccountName: props.userID,
                          domain: props.domain,
                          passkey: props.session_passkey
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
                  if (data.data[row].pc_id == pc_id_input_line.value) {
                    new_row_from_api = JSON.parse(JSON.stringify(data.data[row]));
                    data.data[row]['save'] = "Save";
                    data.data[row]['cancel'] = "Cancel";
                    data.data[row]['delete'] = "Delete";
                    data.data[row]['colorcode'] = 'edited';
                    //console.info('updating a row with: ' + target_url);
                    //console.info(data.data[row]);
                    
                    var new_orig_rows = JSON.parse(JSON.stringify(props.origRows));
                    new_orig_rows.push(data.data[row]);
                    //console.info('new_orig_rows');
                    //console.info(new_orig_rows);
                    props.setOrigRows(new_orig_rows);
                    //console.info('origRows');
                    //console.info(props.origRows);
                    props.hospTable.addData([JSON.parse(JSON.stringify(data.data[row]))], true);
                    handleClose();
                    set_error_notification("");
                    set_save_button_disabled(false);
                    set_save_button_text('Save');
                    setTimeout(function() {
                      data.data[row]['save'] = "Save";
                      data.data[row]['colorcode'] = "not edited";
                      props.hospTable.updateData([JSON.parse(JSON.stringify(data.data[row]))]);
                    }, 10000);
                  }
                }
              }
              else {
                set_error_notification("");
                set_save_button_disabled(false);
                set_save_button_text('Save');
                handleClose();
              }
            },
            error: function(jqXHR, textStatus, errorThrown) {
              set_error_notification("");
              set_save_button_disabled(false);
              set_save_button_text('Save');
              handleClose();
            }
      }).then(function(promise_data){
            // add a row to changelog
            //console.info('changelog ajax call()');
            //console.info(promise_data);
            //console.info(self.state.addOrUpdateOneHospitalRow_data);
            //console.info(self.state.addOrUpdateOneHospitalRow_url_args);
            //console.info(self.state.original_rows);
  
            
  
            //console.info(old_pc_id);
            //console.info(old_printer);
            //console.info(self.props);
  
            var log_entry = 'Add new record';
            var notes = JSON.stringify({new_row: new_row_from_api});
            var new_pc_id = pc_id_input_line.value;
            var new_printer = printer_input_line.value;
            var createdby = props.userID;
            var domain = props.domain;
            var createdby_host = props.pchost;
            var environment = 'prod';
  
            var target_url = global.config.conf.api_endpoint + 'addOneChangelogRow';
            var url_args = { log_entry: log_entry,
                              new_pc_id: new_pc_id,
                              new_printer: new_printer,
                              environment: environment,
                              notes: notes,
                              createdby: createdby,
                              createdby_host: createdby_host,
                              samAccountName: props.userID,
                              domain: props.domain,
                              passkey: props.session_passkey
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
              }
            });
          });
        });
    }
  }

  function FormPropsTextFields(props) {
    //console.info('FormPropsTextFields()');
    //console.info(props);
  
    const classes = useStyles();
    const [pc_id_state, set_pc_id_state] = React.useState("");
    const [printer_state, set_printer_state] = React.useState("");
  
    return (
      <form className={classes.root} noValidate autoComplete="off">
        <div>
          <TextField required id="PC-ID-required"
                     label="PC ID"
                     inputRef={(c) => {props.set_pc_id_input_line(c)}} 
                     value={pc_id_state}
                     onChange={event => {set_pc_id_state(event.target.value)}}
                     error={pc_id_state === ""} />
          <TextField required id="Printer-required"
                     label="Printer" 
                     inputRef={(c) => {props.set_printer_input_line(c)}}
                     value={printer_state}
                     onChange={event => {set_printer_state(event.target.value)}}
                     error={printer_state === ""} />
          <TextField id="Notes-required" label="Notes" defaultValue="" inputRef={(c) => {props.set_notes_input_line(c)}} />
        </div>
      </form>
    );
  }


  export default NewRowModal;