const msalConfig = {
  auth: {
    clientId: 'YOUR_AZURE_AD_APP_CLIENT_ID',
    authority: 'https://login.microsoftonline.com/common',
    redirectUri: window.location.origin
  }
};

const loginRequest = {
  scopes: ['openid', 'profile', 'User.read']
};

const msalInstance = new msal.PublicClientApplication(msalConfig);

const userInfo = document.getElementById('user-info');
const employeeIdInput = document.getElementById('employeeId');
const deploymentForm = document.getElementById('deployment-form');
const resultMessage = document.getElementById('resultMessage');

function signIn() {
  msalInstance.loginPopup(loginRequest)
    .then(response => {
      userInfo.textContent = `Signed in as ${response.account.username}`;
      employeeIdInput.value = response.account.localAccountId || response.account.homeAccountId;
    })
    .catch(error => {
      resultMessage.textContent = `Login failed: ${error.message}`;
      resultMessage.style.color = 'red';
    });
}

function submitBuild(event) {
  event.preventDefault();
  if (!employeeIdInput.value) {
    resultMessage.textContent = 'Please sign in with Azure AD before triggering deployment.';
    resultMessage.style.color = 'red';
    return;
  }

  const formData = {
    team_name: document.getElementById('teamName').value,
    product: document.getElementById('product').value,
    team_lead: document.getElementById('teamLead').value,
    team_vip: document.getElementById('teamVip').value,
    budget_id: document.getElementById('budgetId').value,
    employee_id: employeeIdInput.value,
    environment: document.getElementById('environment').value,
    pr_url: document.getElementById('prUrl').value,
    comments: document.getElementById('comments').value
  };

  fetch('/jenkins/trigger', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        resultMessage.textContent = 'Deployment request submitted. Check Jenkins for status.';
        resultMessage.style.color = 'green';
      } else {
        resultMessage.textContent = `Error: ${data.message}`;
        resultMessage.style.color = 'red';
      }
    })
    .catch(error => {
      resultMessage.textContent = `Network error: ${error.message}`;
      resultMessage.style.color = 'red';
    });
}
