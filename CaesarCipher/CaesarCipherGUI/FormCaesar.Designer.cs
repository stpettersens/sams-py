namespace SamsPy
{
    partial class FormCaesar
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.txtArea = new System.Windows.Forms.RichTextBox();
            this.btnGo = new System.Windows.Forms.Button();
            this.rdoEncrypt = new System.Windows.Forms.RadioButton();
            this.rdoDecrypt = new System.Windows.Forms.RadioButton();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Lucida Sans Unicode", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.Location = new System.Drawing.Point(152, 12);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(224, 30);
            this.label1.TabIndex = 0;
            this.label1.Text = "Enter the text to encrypt or decrypt with \r\nthe CaesarCipher library.";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Lucida Sans Unicode", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.Location = new System.Drawing.Point(9, 172);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(143, 30);
            this.label2.TabIndex = 2;
            this.label2.Text = "Ceasar by keepwaddling1\r\n / Flickr CC:BY";
            // 
            // txtArea
            // 
            this.txtArea.Font = new System.Drawing.Font("Lucida Sans Unicode", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtArea.Location = new System.Drawing.Point(155, 54);
            this.txtArea.Name = "txtArea";
            this.txtArea.Size = new System.Drawing.Size(221, 78);
            this.txtArea.TabIndex = 3;
            this.txtArea.Text = "";
            this.txtArea.TextChanged += new System.EventHandler(this.txtArea_TextChanged);
            // 
            // btnGo
            // 
            this.btnGo.Enabled = false;
            this.btnGo.Font = new System.Drawing.Font("Lucida Sans Unicode", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.btnGo.Location = new System.Drawing.Point(246, 136);
            this.btnGo.Name = "btnGo";
            this.btnGo.Size = new System.Drawing.Size(130, 42);
            this.btnGo.TabIndex = 4;
            this.btnGo.Text = "Go";
            this.btnGo.UseVisualStyleBackColor = true;
            this.btnGo.Click += new System.EventHandler(this.btnGo_Click);
            // 
            // rdoEncrypt
            // 
            this.rdoEncrypt.AutoSize = true;
            this.rdoEncrypt.Checked = true;
            this.rdoEncrypt.Font = new System.Drawing.Font("Lucida Sans Unicode", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.rdoEncrypt.Location = new System.Drawing.Point(173, 138);
            this.rdoEncrypt.Name = "rdoEncrypt";
            this.rdoEncrypt.Size = new System.Drawing.Size(66, 19);
            this.rdoEncrypt.TabIndex = 5;
            this.rdoEncrypt.TabStop = true;
            this.rdoEncrypt.Text = "Encrypt";
            this.rdoEncrypt.UseVisualStyleBackColor = true;
            // 
            // rdoDecrypt
            // 
            this.rdoDecrypt.AutoSize = true;
            this.rdoDecrypt.Font = new System.Drawing.Font("Lucida Sans Unicode", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.rdoDecrypt.Location = new System.Drawing.Point(173, 161);
            this.rdoDecrypt.Name = "rdoDecrypt";
            this.rdoDecrypt.Size = new System.Drawing.Size(67, 19);
            this.rdoDecrypt.TabIndex = 6;
            this.rdoDecrypt.Text = "Decrypt";
            this.rdoDecrypt.UseVisualStyleBackColor = true;
            // 
            // pictureBox1
            // 
            this.pictureBox1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.pictureBox1.Image = global::SamsPy.Properties.Resources.Caesar;
            this.pictureBox1.Location = new System.Drawing.Point(12, 12);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(134, 157);
            this.pictureBox1.TabIndex = 1;
            this.pictureBox1.TabStop = false;
            // 
            // FormCaesar
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(396, 215);
            this.Controls.Add(this.rdoDecrypt);
            this.Controls.Add(this.rdoEncrypt);
            this.Controls.Add(this.btnGo);
            this.Controls.Add(this.txtArea);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "FormCaesar";
            this.Text = "CaesarCipher Encrypter/Decrypter";
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.RichTextBox txtArea;
        private System.Windows.Forms.Button btnGo;
        private System.Windows.Forms.RadioButton rdoEncrypt;
        private System.Windows.Forms.RadioButton rdoDecrypt;
    }
}

