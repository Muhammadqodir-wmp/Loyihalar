using System;
using System.Collections.Generic;
using System.Data;
using System.Windows.Forms;
using MySql.Data.MySqlClient;

namespace Oshxonamenyu
{
    public partial class dishesForm : Form
    {
        private MySqlConnection conn;
        private MySqlDataAdapter adapter;
        private DataSet ds;
        private int id_row;

        private Hisob2 hisobForm;
      

        public dishesForm()
        {
            InitializeComponent();
            hisobForm = new Hisob2();
           
            LoadDishes(); // Load dishes data when the form is initialized

        }

        private void LoadDishes()
        {
            string connStr = "server=localhost;database=oshxona;uid=root;password=;";
            string query = "SELECT id, nomi, narxi, miqdori FROM taomlar";

            using (conn = new MySqlConnection(connStr))
            {
                using (adapter = new MySqlDataAdapter(query, conn))
                {
                    ds = new DataSet();
                    adapter.Fill(ds);
                    dataGridView1.DataSource = ds.Tables[0];
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            string connectionString = "server=localhost;database=oshxona;uid=root;password=;";

            using (MySqlConnection connection = new MySqlConnection(connectionString))
            {
                connection.Open();

                foreach (DataGridViewRow row in dataGridView1.Rows)
                {
                    if (!row.IsNewRow)
                    {
                        string nomi = row.Cells["nomi"].Value.ToString();
                        decimal narxi;
                        decimal miqdori;
                        int id;

                        if (decimal.TryParse(row.Cells["narxi"].Value.ToString(), out narxi) &&
                            decimal.TryParse(row.Cells["miqdori"].Value.ToString(), out miqdori) &&
                            int.TryParse(row.Cells["id"].Value.ToString(), out id))
                        {
                            string query = "INSERT INTO taomlar (id, nomi, narxi, miqdori) VALUES (@id, @nomi, @narxi, @miqdori) ON DUPLICATE KEY UPDATE nomi = @nomi, narxi = @narxi, miqdori = @miqdori";

                            using (MySqlCommand cmd = new MySqlCommand(query, connection))
                            {
                                cmd.Parameters.AddWithValue("@id", id);
                                cmd.Parameters.AddWithValue("@nomi", nomi);
                                cmd.Parameters.AddWithValue("@narxi", narxi);
                                cmd.Parameters.AddWithValue("@miqdori", miqdori);

                                cmd.ExecuteNonQuery();
                            }
                        }
                        else
                        {
                            MessageBox.Show("Invalid data format in the DataGridView.");
                        }
                    }
                }
            }

            LoadDishes(); // Refresh DataGridView after insertion
        }

        private void dataGridView1_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            id_row = e.RowIndex;
            dataGridView1.Rows[id_row].Cells["nomi"].Value.ToString();
            dataGridView1.Rows[id_row].Cells["narxi"].Value.ToString();
            dataGridView1.Rows[id_row].Cells["miqdori"].Value.ToString();
            dataGridView1.Rows[id_row].Cells["id"].Value.ToString();
        }

        private void dishesForm_Load(object sender, EventArgs e)
        {

        }
        public dishesForm(Form1 formn)
        {
            InitializeComponent();

        }

        private void button4_Click(object sender, EventArgs e)
        {
            string connectionString = "server=localhost;database=oshxona;uid=root;password=;";
            if (dataGridView1.SelectedRows.Count > 0)
            {
                // Get the selected row
                DataGridViewRow selectedRow = dataGridView1.SelectedRows[0];

                // Get the value of the primary key column (adjust the column index accordingly)
                int primaryKeyValue = Convert.ToInt32(selectedRow.Cells["id"].Value);

                // Your MySQL query to delete the selected row
                string deleteQuery = "DELETE FROM taomlar WHERE id = @PrimaryKeyValue";

                using (MySqlConnection connection = new MySqlConnection(connectionString))
                {
                    connection.Open();

                    using (MySqlCommand cmd = new MySqlCommand(deleteQuery, connection))
                    {
                        cmd.Parameters.AddWithValue("@PrimaryKeyValue", primaryKeyValue);
                        cmd.ExecuteNonQuery();
                    }
                }

                // Remove the selected row from the DataGridView
                dataGridView1.Rows.Remove(selectedRow);
            }
            else
            {
                MessageBox.Show("Please select a row to delete.", "Delete Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }

        }

        private void button5_Click(object sender, EventArgs e)
        {
            hisobForm.Show();
            this.Hide();
        }

      
    }
}
