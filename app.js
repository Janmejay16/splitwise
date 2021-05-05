(function () {
  'use strict'
    angular.module('MsgApp', [])
    .controller('MsgController', MsgController)
    .filter('passwordFilter',function() {
      return function(input) {
        var res = ""
        for (var i=0;i<input.length;i++) {
          res+="*"
        }
        return res
      }
    })
    .filter('dates',function() {
      return function(input) {
        var res = ""
        res+= input.slice(5,7) + " " + input.slice(8,11) + " " + input.slice(12,16) + ", " + input.slice(0,3)
        return res
      }
    });
    MsgController.$inject = ['$scope','$http']
    function MsgController($scope,$http) {
      $scope.allusers=[]
      $scope.alltransactions=[]
      $scope.allaccounts=[]
      $scope.individualTrans = null
      $scope.userTrans = false;
      $scope.addTrans = false;
      $scope.currentUser=null
      $scope.username=""
      $scope.password=""
      $scope.users= ""
      $scope.amount= ""
      $scope.transaction_date= ""
      $scope.month = ""
      $scope.year = ""
      $scope.date = ""
      $scope.viewUsers = false;
      $scope.viewTran = false;
      $scope.viewAcc = false;
      $scope.notLoggedIn=true;
      $scope.signin=true;
      $scope.signup=false;
      $scope.admin = false;
      $scope.seepassword = false;
      $scope.addTrans = false;
      $scope.newTransactions = []

      $scope.addEntry = function () {
        var entry = {
          "user": $scope.users,
          "amount": $scope.amount
        }
        $scope.newTransactions.push(entry)
      }

      $scope.seepasswordfunc = function() {
          if ($scope.seepassword==true) {
            $scope.seepassword = false;
          }
          else {
            $scope.seepassword = true;
          }
      }

      $scope.addTransSection = function () {
        if($scope.addTrans == false) $scope.addTrans = true;
        else if($scope.addTrans == true) $scope.addTrans = false; 
      }
 
      $scope.changeToSignUp = function() {
        $scope.signin = false;
        $scope.signup = true;
      }

      $scope.changeToSignIn = function() {
        $scope.signup = false;
        $scope.signin = true;
      }

      $scope.logout = function () {
        $scope.allusers=[]
        $scope.alltransactions=[]
        $scope.allaccounts=[]
        $scope.individualTrans = null
        $scope.userTrans = false;
        $scope.addTrans = false;
        $scope.currentUser=null
        $scope.username=""
        $scope.password=""
        $scope.users= ""
        $scope.amount= ""
        $scope.transaction_date= ""
        $scope.month = ""
        $scope.year = ""
        $scope.date = ""
        $scope.viewUsers = false;
        $scope.viewTran = false;
        $scope.viewAcc = false;
        $scope.notLoggedIn=true;
        $scope.signin=true;
        $scope.signup=false;
        $scope.admin = false;
        $scope.seepassword = false;
        $scope.addTrans = false;
        $scope.newTransactions = []
      }
        
        $scope.clearAddTrans = function() {
          $scope.newTransactions = []
        }

      $scope.showTrans = function () {
        $scope.viewTran = true;
      }
      
      $scope.fetchUsers = function() {
        $http({
          method: 'GET',
          url: 'https://webtech-angular-backend.herokuapp.com/users'
        })
        .then(response => {
          if (response.data.success==true) {
            var users_list = []
            response.data.users.map(user => {
              users_list.push({
                id: user.id,
                username: user.username,
                password: user.password
              })
            })
            $scope.allusers = users_list
            $scope.viewUsers = true
          }
        }, err => {
          console.log(err)
        })
      }
      $scope.hideUsers = function() {
        $scope.viewUsers = false
      }
      $scope.hideTran = function() {
        $scope.viewTran = false
      }
      $scope.hideUserTrans = function() {
        $scope.userTrans = false
      }
      $scope.hideAcc = function() {
        $scope.viewAcc = false
      }
      $scope.fetchTransactions = function() {
        $http({
          method: 'GET',
          url: 'https://webtech-angular-backend.herokuapp.com/transactions'
        })
        .then(response => {
          if (response.data.success==true) {
            var transactions_list = []
            response.data.transactions.map(transaction => {
              transactions_list.push({
                id: transaction.id,
                transactions_date: transaction.transactions_date,
                users: transaction.users,
                amount: transaction.amount,
                user_id: transaction.user_id,
                transaction_date: transaction.transaction_date,
              })
            })
            $scope.alltransactions = transactions_list
            $scope.viewTran = true
          }
        }, err => {
          console.log(err)
        })
      }

      $scope.login = function() {
        $http({
          method: 'POST',
          url: 'https://webtech-angular-backend.herokuapp.com/login',
          data: {
            username: $scope.username,
            password: $scope.password
          }
        })
        .then(response => {
          if (response.data.success==true) {
            $scope.currentUser = response.data.user
            console.log($scope.currentUser)
            alert(response.data.message);
            $scope.notLoggedIn=false;
            if (response.data.user.username == "admin") {
              $scope.admin = true;
              alert('admin')
            }
          }
          else {
            alert(response.data.message)
          }
        }, err => {
          console.log(err)
        })
      }

      $scope.register = function() {
        $http({
          method: 'POST',
          url: 'https://webtech-angular-backend.herokuapp.com/register',
          data: {
            username: $scope.username,
            password: $scope.password
          }
        })
        .then(response => {
          if (response.data.success==true) {
            $scope.currentUser = response.data.user
            console.log($scope.currentUser)
            alert(response.data.message)
            $scope.notLoggedIn=false;
          }
          else {
            alert(response.data.message)
          }
        }, err => {
          console.log(err)
        })
      }

      $scope.viewtrans = function() {
        if ($scope.currentUser) {
          $http({
            method: 'GET',
            url: 'https://webtech-angular-backend.herokuapp.com/transactions/'+$scope.currentUser.id
          })
          .then(response => {
            console.log(response.data)
            if (response.data.success==true) {
              $scope.individualTrans = response.data.transactions
              console.log($scope.individualTrans)
              $scope.userTrans=true;
            }
          }, err => {
            console.log(err)
          })
        }
        else {
          alert('You must be logged In!')
        }
      }

      $scope.addtransaction = function() {
        var users = []
        var amount = []
        for (var i=0;i<$scope.newTransactions.length;i++) {
          console.log($scope.newTransactions)
          users.push($scope.newTransactions[i].user)
          amount.push($scope.newTransactions[i].amount)
        }
        users = users.join(",")
        amount = amount.join(",")
        if ($scope.currentUser) {
          var data = {
            user_id: $scope.currentUser.id,
            users: users,
            amount: amount,
            transaction_date: $scope.year+"/"+$scope.month+"/"+$scope.date
          }
          console.log(data)
          $http({
            method: 'POST',
            url: 'https://webtech-angular-backend.herokuapp.com/transaction',
            data: data
          })
          .then(response => {
            console.log(data)
            console.log(response.data)
            if (response.data.success==true) {
              $scope.currentUser = response.data.user
              console.log($scope.currentUser)
            }
          }, err => {
            console.log(err)
          })
        }
        else {
          alert('You must be logged In!')
        }
      }
      $scope.fetchAccounts = function() {
        let url = 'https://webtech-angular-backend.herokuapp.com/accounts/'+$scope.currentUser.id
        // alert(url)
        if ($scope.currentUser) {
          $http({
            method: 'GET',
            url: url
          })
          .then(response => {
            if (response.data.success == true) {
              var accounts_list = []
              response.data.accounts.map(account => {
                accounts_list.push({
                  id: account.id,
                  transaction_id: account.transaction_id,
                  transaction_date: account.transaction_date,
                  amount: account.amount,
                  receiver: account.receiver,
                  lender: account.lender,
                })
              })
              $scope.allaccounts = accounts_list
              $scope.viewAcc = true
            }
          })
        }
        else alert('You must be Logged In!')
      }
      $scope.checkLogin = function () {
        console.log("Checked of Logged In!")
        if($scope.currentUser!=null) {
          $scope.notLoggedIn = false;
          if ($scope.currentUser.username == "admin") $scope.admin = false;
          $scope.signin = false;
        }
        else {
          $scope.notLoggedIn = true;
          $scope.currentUser = null;
          $scope.admin = false;
          $scope.signin = true;
        }
      }
      $scope.checkLogin();
    }
})();