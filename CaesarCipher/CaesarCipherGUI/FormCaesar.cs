//
// Main and only window
//
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

namespace SamsPy {
    public partial class FormCaesar : Form {
        public FormCaesar() {
            InitializeComponent();
        }

        private void btnGo_Click(object sender, EventArgs e) {
            if(this.rdoEncrypt.Checked) {
                this.txtArea.Text = 
                CaesarCipherGUI.encrypt(this.txtArea.Text);
            }
            else this.txtArea.Text = CaesarCipherGUI.decrypt(this.txtArea.Text);

        }

        private void txtArea_TextChanged(object sender, EventArgs e) {
            if(txtArea.Text.Length > 2) this.btnGo.Enabled = true;
            else this.btnGo.Enabled = false;
        }
    }
}
