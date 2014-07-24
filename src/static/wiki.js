angular.module('wiki', [])
	.controller('DocumentListController', function ($scope, $http) {
		$scope.reload = function () {
			$http.get('/documentList')
				.then(function (result) {
					$scope.documentList = result.data;
				});
		};
		
		$scope.documentList = [];
		$scope.reload();
	})
	.controller('InvoiceCounterController', function ($scope, $http) {
		$scope.generateInvoiceNumber = function () {
			$http.post('/invoiceNumber')
				.then(function (result) {
					if (result.data) {
						$scope.invoiceNumber = result.data.invoiceNumber;
					}
				})
		};
	});