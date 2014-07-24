angular.module('wiki', [])
	.controller('DocumentListController', function ($scope, $rootScope, $http) {
		$scope.reload = function () {
			$http.get('/documentList')
				.then(function (result) {
					$scope.documentList = result.data;
				});
		};
		
		$scope.preview = function (doc) {
			$rootScope.$broadcast('previewDocument', doc);
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
	})
	.controller('PreviewController', function ($scope, $rootScope, $sce) {
		$scope.isImage = function (doc) {
			return doc !== undefined && doc.mimetype.match(/^image\//) != null;
		};
		
		$scope.isPdf = function (doc) {
			return doc !== undefined && doc.mimetype === 'application/pdf';
		}
		
		$scope.$on('previewDocument', function (event, doc) {
			$scope.documentUrl = $sce.trustAsResourceUrl('document/' + doc.name);
			$scope.doc = doc;
		});
	});